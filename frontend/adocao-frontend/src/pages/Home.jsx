import { useEffect, useMemo, useState } from "react";
import { api } from "../services/api";
import { useNavigate } from "react-router-dom";
import SwipeDeck from "../components/SwipeDeck";

const API_URL = "http://127.0.0.1:8000";

function safeJsonParse(str) {
  if (!str) return null;
  if (str === "undefined" || str === "null") return null;
  try {
    return JSON.parse(str);
  } catch {
    return null;
  }
}

function roleLabel(role) {
  if (role === "ADOTANTE") return "Adotante";
  if (role === "ONG") return "ONG";
  if (role === "DOADOR") return "Doador";
  return role || "Usuário";
}

function areaButtonLabel(role) {
  if (role === "ADOTANTE") return "Acompanhar minhas solicitações";
  if (role === "ONG") return "Gerenciar animais e pedidos";
  if (role === "DOADOR") return "Minha área";
  return "Minha área";
}

function SkeletonCard() {
  return (
    <div className="card">
      <div className="skeleton skeleton-image" />
      <div className="card-row">
        <div className="card-main skeleton-stack">
          <div className="skeleton skeleton-line big" />
          <div className="skeleton skeleton-line medium" />
        </div>
        <div className="skeleton skeleton-line small" />
      </div>
    </div>
  );
}

export default function Home() {
  const navigate = useNavigate();

  const [animals, setAnimals] = useState([]);
  const [err, setErr] = useState(null);
  const [loadingAnimals, setLoadingAnimals] = useState(true);

  const token = localStorage.getItem("token");
  const user = useMemo(
    () => safeJsonParse(localStorage.getItem("currentUser")),
    []
  );

  // limpa estado inconsistente
  useEffect(() => {
    if (token && !user) {
      localStorage.removeItem("token");
      localStorage.removeItem("currentUser");
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // carrega animais
  useEffect(() => {
    async function loadAnimals() {
      setErr(null);
      setLoadingAnimals(true);
      try {
        const data = await api("/animals");
        setAnimals(Array.isArray(data) ? data : data?.items || []);
      } catch (e) {
        setErr(e.message || "Erro ao carregar animais.");
      } finally {
        setLoadingAnimals(false);
      }
    }
    loadAnimals();
  }, []);

  function handleLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("currentUser");
    navigate("/login");
  }

  function goDashboard() {
    const t = localStorage.getItem("token");
    const u = safeJsonParse(localStorage.getItem("currentUser"));

    if (!t || !u) {
      navigate("/login");
      return;
    }

    if (u.role === "ONG") navigate("/dashboard/ong");
    else if (u.role === "ADOTANTE") navigate("/dashboard/adotante");
    else if (u.role === "DOADOR") navigate("/dashboard/doador");
    else navigate("/dashboard");
  }

  // ✅ B: backend único /animals/:id/react
  async function onReact(animal, kind) {
    const t = localStorage.getItem("token");
    const u = safeJsonParse(localStorage.getItem("currentUser"));

    if (!t || !u) {
      alert("Faça login para interagir com os animais.");
      navigate("/login");
      return null;
    }

    // Se quiser restringir curtida só a ADOTANTE:
    // if (u.role !== "ADOTANTE") {
    //   alert("Somente contas de Adotante podem curtir.");
    //   return null;
    // }

    const data = await api(`/animals/${animal.id}/react`, {
      method: "POST",
      body: { kind }, // "LIKE" | "DISLIKE" | "SUPERLIKE"
    });

    // ✅ atualiza o animal na lista local para refletir like_count/liked_by_me
    setAnimals((prev) =>
      prev.map((a) =>
        a.id === animal.id
          ? {
              ...a,
              like_count: data.like_count,
              liked_by_me: data.liked_by_me,
              my_kind: data.my_kind ?? a.my_kind,
            }
          : a
      )
    );

    // retorna um animal atualizado (pra SwipeDeck abrir perfil certo no SUPERLIKE)
    return {
      ...animal,
      like_count: data.like_count,
      liked_by_me: data.liked_by_me,
      my_kind: data.my_kind ?? animal.my_kind,
    };
  }

  const currentUser = safeJsonParse(localStorage.getItem("currentUser"));
  const isLogged = !!localStorage.getItem("token") && !!currentUser;

  // deck tinder: só disponíveis + capa
  const availableAnimals = useMemo(() => {
    return animals
      .filter((a) => a.available)
      .map((a) => ({
        ...a,
        __cover: a.image_url ? `${API_URL}${a.image_url}` : null,
      }));
  }, [animals]);

  return (
    <div className="container">
      <div className="header">
        <div>
          <div className="brand">
            <div style={{ fontSize: 40 }}>🐶</div>
            <h1>AdoCÃO</h1>
          </div>

          {isLogged ? (
            <p className="subtitle">
              Logado como: <b>{currentUser.name}</b> ({roleLabel(currentUser.role)})
            </p>
          ) : (
            <p className="subtitle">Encontre seu novo amigo para adoção 🐾</p>
          )}
        </div>

        <div className="actions">
          {isLogged ? (
            <>
              <button className="btn btn-primary" onClick={goDashboard}>
                {areaButtonLabel(currentUser.role)}
              </button>

              {currentUser.role === "ONG" && (
                <button className="btn" onClick={() => navigate("/animals/new")}>
                  ➕ Cadastrar novo animal
                </button>
              )}

              <button className="btn btn-danger" onClick={handleLogout}>
                Sair
              </button>
            </>
          ) : (
            <>
              <button className="btn btn-primary" onClick={() => navigate("/login")}>
                Entrar
              </button>
              <button className="btn" onClick={() => navigate("/register")}>
                Criar conta
              </button>
            </>
          )}
        </div>
      </div>

      <hr className="divider" />
      <h2 className="section-title">🐾 Animais disponíveis</h2>

      {err && <p style={{ color: "crimson" }}>Erro ao carregar: {err}</p>}

      {!err && loadingAnimals ? (
        <>
          <SkeletonCard />
          <SkeletonCard />
          <SkeletonCard />
        </>
      ) : !err && availableAnimals.length === 0 ? (
        <p className="muted">Nenhum animal disponível ainda.</p>
      ) : (
        <SwipeDeck
          animals={availableAnimals}
          onReact={onReact}
          onOpen={(animal) => navigate(`/animals/${animal.id}`)}
        />
      )}
    </div>
  );
}
