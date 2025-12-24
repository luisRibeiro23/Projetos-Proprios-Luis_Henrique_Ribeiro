import { useEffect, useMemo, useRef, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api } from "../services/api";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";


function safeJsonParse(str) {
  try {
    return JSON.parse(str || "null");
  } catch {
    return null;
  }
}

export default function AnimalProfile() {
  const { id } = useParams();
  const navigate = useNavigate();
  const user = safeJsonParse(localStorage.getItem("currentUser"));

  const [animal, setAnimal] = useState(null);
  const [err, setErr] = useState(null);
  const [loading, setLoading] = useState(true);

  // carrossel
  const [imgIdx, setImgIdx] = useState(0);

  // upload multi-fotos (só ONG dona)
  const fileRef = useRef(null);
  const [uploading, setUploading] = useState(false);

  // ===== adoção =====
  const [myRequests, setMyRequests] = useState([]);
  const [adopting, setAdopting] = useState(false);

  async function load() {
    setErr(null);
    setLoading(true);
    try {
      const data = await api(`/animals/${id}`);
      setAnimal(data);
      setImgIdx(0);

      // carrega minhas solicitações (se logado)
      const token = localStorage.getItem("token");
      const currentUser = safeJsonParse(localStorage.getItem("currentUser"));
      if (token && currentUser) {
        const dataReqs = await api("/adoption-requests");
        const listReqs = Array.isArray(dataReqs) ? dataReqs : dataReqs?.items || [];
        setMyRequests(listReqs);
      } else {
        setMyRequests([]);
      }
    } catch (e) {
      setErr(e.message || "Erro ao carregar animal.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const isOwnerONG = useMemo(() => {
    if (!animal || !user) return false;
    return user.role === "ONG" && Number(animal.owner_id) === Number(user.id);
  }, [animal, user]);

  const images = useMemo(() => {
    if (!animal) return [];
    const list = [];

    if (animal.image_url) list.push(`${API_URL}${animal.image_url}`);

    if (Array.isArray(animal.photos)) {
      for (const p of animal.photos) {
        if (p?.url) list.push(`${API_URL}${p.url}`);
      }
    }

    return Array.from(new Set(list));
  }, [animal]);

  function nextImg() {
    const len = images.length;
    if (!len) return;
    setImgIdx((v) => (v + 1) % len);
  }

  function prevImg() {
    const len = images.length;
    if (!len) return;
    setImgIdx((v) => (v - 1 + len) % len);
  }

  async function uploadPhotos(e) {
    const files = Array.from(e.target.files || []);
    if (!files.length) return;

    const fd = new FormData();
    for (const f of files) fd.append("files", f);

    try {
      setUploading(true);
      const updated = await api(`/animals/${animal.id}/photos`, {
        method: "POST",
        body: fd,
      });
      setAnimal(updated);
      setImgIdx(0);
      alert("Fotos adicionadas!");
    } catch (err) {
      alert("Erro ao enviar fotos: " + (err.message || "erro"));
    } finally {
      setUploading(false);
      if (fileRef.current) fileRef.current.value = "";
    }
  }

  // ===== lógica de bloquear solicitação =====
  const isLogged = !!localStorage.getItem("token") && !!user;
  const isAdotante = user?.role === "ADOTANTE";

  const hasBlockingRequest = useMemo(() => {
    const animalId = Number(id);
    return (myRequests || []).some((r) => {
      const rid = Number(r.animal_id ?? r.animal?.id);
      const st = (r.status || "").toUpperCase();
      return rid === animalId && (st === "PENDENTE" || st === "APROVADO");
    });
  }, [myRequests, id]);

  async function handleAdopt() {
    if (!isLogged) {
      navigate("/login");
      return;
    }
    if (!isAdotante) return; // silencioso
    if (!animal?.available) return;
    if (hasBlockingRequest) return;

    try {
      setAdopting(true);

      await api("/adoption-requests", {
        method: "POST",
        body: JSON.stringify({
          animal_id: Number(id),
          message: "Gostaria de adotar este animal",
        }),
      });

      // atualiza requests pra travar o botão
      const dataReqs = await api("/adoption-requests");
      const listReqs = Array.isArray(dataReqs) ? dataReqs : dataReqs?.items || [];
      setMyRequests(listReqs);
    } catch (e) {
      // se backend responder algo tipo "já existe", a lista acima já travaria;
      // aqui só cai em erro inesperado
      alert(e.message || "Erro ao enviar solicitação.");
    } finally {
      setAdopting(false);
    }
  }

  if (loading)
    return (
      <div className="container">
        <p className="muted">Carregando...</p>
      </div>
    );
  if (err)
    return (
      <div className="container">
        <p style={{ color: "crimson" }}>{err}</p>
      </div>
    );
  if (!animal) return null;

  const cover = images[imgIdx] || null;

  const adoptDisabled =
    adopting ||
    !animal.available ||
    hasBlockingRequest ||
    !isLogged ||
    !isAdotante;

  const adoptText = !isLogged
    ? "Entrar para solicitar adoção"
    : !isAdotante
    ? "Apenas adotante pode solicitar"
    : !animal.available
    ? "Indisponível"
    : hasBlockingRequest
    ? "Solicitação já enviada"
    : adopting
    ? "Enviando..."
    : "Quero adotar";

  return (
    <div className="container">
      <div className="header">
        <div>
          <div className="brand">
            <div style={{ fontSize: 34 }}>🐾</div>
            <h1>{animal.name}</h1>
          </div>
          <p className="subtitle">
            {animal.species} • {animal.city}/{animal.state} • {animal.size}
          </p>
        </div>

        <div className="actions">
          <button className="btn" onClick={() => navigate(-1)}>
            ← Voltar
          </button>
          <button className="btn" onClick={() => navigate("/")}>
            Home
          </button>
        </div>
      </div>

      <hr className="divider" />

      <div className="tinder-stage">
        <div className="tinder-card">
          <div className="tinder-media">
            {cover ? <img src={cover} alt={animal.name} /> : <div className="tinder-media-fallback">🐾</div>}

            <div className="tinder-badges">
              <span className="pill">{animal.size}</span>
              {animal.age ? <span className="pill">{animal.age}</span> : null}
              <span className="pill pill-right">❤️ {animal.like_count ?? 0}</span>
            </div>

            {images.length > 1 && (
              <>
                <button className="carousel-btn left" onClick={prevImg} aria-label="Anterior">
                  ‹
                </button>
                <button className="carousel-btn right" onClick={nextImg} aria-label="Próxima">
                  ›
                </button>

                <div className="carousel-dots">
                  {images.map((_, i) => (
                    <span key={i} className={`dot ${i === imgIdx ? "active" : ""}`} />
                  ))}
                </div>
              </>
            )}
          </div>

          <div className="tinder-info">
            <div className="tinder-sub">
              {animal.species} • {animal.city}/{animal.state}
            </div>

            {animal.description ? (
              <div className="tinder-about">{animal.description}</div>
            ) : (
              <div className="tinder-about muted">Sem descrição ainda.</div>
            )}

            {/* ===== BOTÃO DE ADOÇÃO (ADOTANTE) ===== */}
            {!isOwnerONG && (
              <div style={{ marginTop: 12, display: "flex", gap: 10, flexWrap: "wrap" }}>
                <button
                  className="btn btn-primary"
                  disabled={adoptDisabled}
                  onClick={handleAdopt}
                >
                  {adoptText}
                </button>

                {/* opcional: se não logado, deixa um atalho explícito */}
                {!isLogged && (
                  <button className="btn" onClick={() => navigate("/login")}>
                    Fazer login
                  </button>
                )}
              </div>
            )}

            {/* ===== upload (ONG dona) ===== */}
            {isOwnerONG && (
              <div style={{ marginTop: 12 }}>
                <input
                  ref={fileRef}
                  type="file"
                  accept="image/*"
                  multiple
                  onChange={uploadPhotos}
                  style={{ display: "none" }}
                  disabled={uploading}
                />
                <button
                  className="btn btn-primary"
                  onClick={() => fileRef.current?.click()}
                  disabled={uploading}
                >
                  {uploading ? "Enviando..." : "➕ Adicionar mais fotos"}
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
