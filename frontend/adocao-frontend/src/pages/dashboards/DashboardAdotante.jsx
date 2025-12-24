import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../../services/api";

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

function animalCover(a) {
  if (!a || !a.image_url) return null;
  if (String(a.image_url).startsWith("http")) return a.image_url;
  return `${API_URL}${a.image_url}`;
}

function openAnimalProfile(animalId) {
  navigate(`/animals/${animalId}`);
}


export default function DashboardAdotante() {
  const navigate = useNavigate();

  const user = useMemo(
    () => safeJsonParse(localStorage.getItem("currentUser")),
    []
  );

  const [animals, setAnimals] = useState([]);
  const [requests, setRequests] = useState([]);
  const [err, setErr] = useState(null);
  const [loading, setLoading] = useState(true);
  const [loadingId, setLoadingId] = useState(null);

  const availableAnimals = useMemo(
    () => animals.filter((a) => a.available),
    [animals]
  );

  async function loadAll() {
    setErr(null);
    setLoading(true);

    try {
      const dataAnimals = await api("/animals");
      setAnimals(Array.isArray(dataAnimals) ? dataAnimals : dataAnimals?.items || []);

      const dataReqs = await api("/adoption-requests");
      setRequests(Array.isArray(dataReqs) ? dataReqs : dataReqs?.items || []);
    } catch (e) {
      setErr(e.message || "Erro ao carregar dados.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadAll();
  }, []);

  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("currentUser");
    navigate("/login");
  }

  // ===== Requests por animal =====
  const requestsByAnimal = useMemo(() => {
    const map = {};
    for (const r of requests) {
      const id = r.animal_id ?? r.animal?.id;
      if (!id) continue;
      map[id] = map[id] || [];
      map[id].push(r);
    }
    return map;
  }, [requests]);

  const animalById = useMemo(() => {
    const m = {};
    for (const a of animals) m[a.id] = a;
    return m;
  }, [animals]);

  function hasBlockingRequest(animalId) {
    const rs = requestsByAnimal[animalId] || [];
    return rs.some((r) =>
      ["PENDENTE", "APROVADO"].includes((r.status || "").toUpperCase())
    );
  }

  async function handleAdopt(animalId) {
    if (hasBlockingRequest(animalId)) return;

    try {
      setLoadingId(animalId);

      await api("/adoption-requests", {
        method: "POST",
        body: JSON.stringify({
          animal_id: animalId,
          message: "Gostaria de adotar este animal",
        }),
      });

      const dataReqs = await api("/adoption-requests");
      setRequests(Array.isArray(dataReqs) ? dataReqs : dataReqs?.items || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingId(null);
    }
  }
  return (
    <div className="container">
      {/* ===== Header ===== */}
      <div className="header">
        <div>
          <h1 className="pageTitle">🙋 Dashboard Adotante</h1>
          <p className="pageSub">
            Logado como: <b>{user?.name || "Usuário"}</b>
          </p>
        </div>

        <div className="actions">
          <button className="btn" onClick={() => navigate("/")}>Home</button>
          <button className="btn danger" onClick={logout}>Sair</button>
        </div>
      </div>

      <hr />

      {/* ===== Animais disponíveis ===== */}
      <h2 className="sectionTitle">🐾 Animais disponíveis</h2>

      {loading && <p className="muted">Carregando dados...</p>}
      {err && <p style={{ color: "crimson" }}>Erro: {err}</p>}

      {!loading && !err && (
        <>
          {availableAnimals.length === 0 ? (
            <div className="card">
              <p className="muted" style={{ margin: 0 }}>
                Nenhum animal disponível no momento.
              </p>
            </div>
          ) : (
            <div className="list">
              {availableAnimals.map((animal) => {
                const blocked = hasBlockingRequest(animal.id);

                return (
                  <div key={animal.id} className="card">
                    <div className="itemTop">

                      {/* FOTO */}
                      <div
                        className="animalThumb clickable"
                        onClick={() => navigate(`/animals/${animal.id}`)}
                      >
                        {animalCover(animal) ? (
                          <img src={animalCover(animal)} alt={animal.name} />
                        ) : (
                          <div className="animalThumbFallback">🐾</div>
                        )}
                      </div>

                      <div className="stack" style={{ flex: 1 }}>
                        <strong
                          className="animalNameLink"
                          onClick={() => navigate(`/animals/${animal.id}`)}
                        >
                          {animal.name}
                        </strong>

                        <span className="muted">
                          {animal.species} — {animal.city}/{animal.state}
                        </span>

                        <div className="row">
                          <span className="badge success">Disponível</span>
                          {blocked && (
                            <span className="badge warn">
                              Solicitação já enviada
                            </span>
                          )}
                        </div>
                      </div>

                      <div className="actions">
                        <button
                          className="btn primary"
                          disabled={blocked || loadingId === animal.id}
                          onClick={() => handleAdopt(animal.id)}
                        >
                          {loadingId === animal.id
                            ? "Enviando..."
                            : blocked
                            ? "Solicitação já enviada"
                            : "Quero adotar"}
                        </button>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </>
      )}

      <hr />

      {/* ===== Minhas solicitações ===== */}
      <h2 className="sectionTitle">📌 Minhas solicitações</h2>

      {requests.length === 0 ? (
        <div className="card">
          <p className="muted" style={{ margin: 0 }}>
            Você ainda não fez nenhuma solicitação.
          </p>
        </div>
      ) : (
        <div className="list">
          {requests
            .slice()
            .sort((a, b) => (b.id || 0) - (a.id || 0))
            .map((r) => {
              const status = (r.status || "").toUpperCase();
              const animal = animalById[r.animal_id];

              return (
                <div
                  key={r.id}
                  className={`card dim ${
                    status === "APROVADO"
                      ? "sucessOutline"
                      : status === "REJEITADO"
                      ? "dangerOutline"
                      : "warnOutline"
                  }`}
                >
                  <div className="itemTop">

                    {/* FOTO */}
                    <div
                      className="animalThumb clickable"
                      onClick={() => animal && navigate(`/animals/${animal.id}`)}
                    >
                      {animalCover(animal) ? (
                        <img src={animalCover(animal)} alt={animal?.name || "Animal"} />
                      ) : (
                        <div className="animalThumbFallback">🐾</div>
                      )}
                    </div>

                    <div className="stack">
                      <div className="row">
                        <strong>Pedido #{r.id}</strong>
                        <span
                          className={`badge ${
                            status === "APROVADO"
                              ? "success"
                              : status === "REJEITADO"
                              ? "danger"
                              : "warn"
                          }`}
                        >
                          {status}
                        </span>
                      </div>

                      {animal && (
                        <span
                          className="animalNameLink"
                          onClick={() => navigate(`/animals/${animal.id}`)}
                        >
                          {animal.name} — {animal.species}
                        </span>
                      )}

                      {r.message && (
                        <span className="muted">
                          Mensagem: “{r.message}”
                        </span>
                      )}

                      {status === "APROVADO" && (
                        <span className="hint">
                          🎉 A ONG aprovou sua solicitação!
                        </span>
                      )}
                      {status === "PENDENTE" && (
                        <span className="hint">
                          ⏳ Sua solicitação está em análise.
                        </span>
                      )}
                      {status === "REJEITADO" && (
                        <span className="hint">
                          ❌ Esta solicitação foi rejeitada.
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
        </div>
      )}
    </div>
  );

}
