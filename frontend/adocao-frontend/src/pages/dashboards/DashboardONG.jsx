import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../../services/api";
import "../../styles/dashboard.css";
import DashboardShell from "../../components/DashboardShell";


function safeJsonParse(str) {
  if (!str) return null;
  if (str === "undefined" || str === "null") return null;
  try {
    return JSON.parse(str);
  } catch {
    return null;
  }
}

export default function DashboardONG() {
  const navigate = useNavigate();

  const user = useMemo(
    () => safeJsonParse(localStorage.getItem("currentUser")),
    []
  );

  const [animals, setAnimals] = useState([]);
  const [requests, setRequests] = useState([]);

  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);

  // para desabilitar botões durante ações
  const [actingId, setActingId] = useState(null);

  async function loadAll() {
    setErr(null);
    setLoading(true);

    try {
      // ✅ 1) animais da ONG (seu backend aceita)
      const myAnimals = await api("/animals?mine=true");
      const animalList = Array.isArray(myAnimals) ? myAnimals : (myAnimals?.items || []);
      setAnimals(animalList);

      // ✅ 2) requests da ONG (agora existe GET e no backend filtra por owner_id)
      const reqs = await api("/adoption-requests");
      const reqList = Array.isArray(reqs) ? reqs : (reqs?.items || []);
      setRequests(reqList);
    } catch (e) {
      setErr(e.message || "Erro ao carregar dashboard.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadAll();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("currentUser");
    navigate("/login");
  }

  // agrupar requests por animal_id
  const requestsByAnimal = useMemo(() => {
    const map = {};
    for (const r of requests) {
      const animalId = r.animal_id ?? r.animal?.id;
      if (!animalId) continue;
      map[animalId] = map[animalId] || [];
      map[animalId].push(r);
    }
    return map;
  }, [requests]);

  function StatusBadge({ status }) {
    const s = (status || "").toUpperCase();
    let cls = "status-pending";
    if (s === "APROVADO") cls = "status-available";
    if (s === "REJEITADO") cls = "status-unavailable";
    return <span className={cls}>{s || "PENDENTE"}</span>;
  }

  // ✅ aprovar/rejeitar via PATCH
  async function setRequestStatus(requestId, status) {
    setActingId(requestId);
    try {
      await api(`/adoption-requests/${requestId}`, {
        method: "PATCH",
        body: JSON.stringify({ status }),
      });

      await loadAll();
    } catch (e) {
      alert(e.message || "Erro ao atualizar solicitação.");
    } finally {
      setActingId(null);
    }
  }

  // ✅ toggle disponibilidade do animal
  async function setAnimalAvailability(animalId, available) {
    setActingId(`animal-${animalId}`);
    try {
      await api(`/animals/${animalId}`, {
        method: "PATCH",
        body: JSON.stringify({ available }),
      });
      await loadAll();
    } catch (e) {
      alert(e.message || "Erro ao atualizar animal.");
    } finally {
      setActingId(null);
    }
  }
  return (
    <DashboardShell
      title="🏠 Dashboard ONG"
      subtitle={
        <>
          Logado como: <b>{user?.name}</b>
        </>
      }
      actions={
        <>
          <button
            className="btn primary"
            onClick={() => navigate("/dashboard/ong/animais/novo")}
          >
            ➕ Cadastrar animal
          </button>

          <button className="btn" onClick={() => navigate("/")}>
            Home
          </button>

          <button className="btn danger" onClick={logout}>
            Sair
          </button>
        </>
      }
    >
      {loading && <p className="muted">Carregando informações...</p>}
      {err && <p style={{ color: "crimson" }}>Erro: {err}</p>}

      {!loading && !err && (
        <>
          <h2 className="sectionTitle">🐾 Seus animais</h2>

          {animals.length === 0 ? (
            <div className="card">
              <p className="muted" style={{ margin: 0 }}>
                Nenhum animal cadastrado ainda.
              </p>
            </div>
          ) : (
            <div className="list">
              {animals.map((a) => {
                const animalReqs = (requestsByAnimal[a.id] || [])
                  .slice()
                  .sort((x, y) => (y.id || 0) - (x.id || 0));

                const pending = animalReqs.filter(
                  (r) => (r.status || "").toUpperCase() === "PENDENTE"
                );

                return (
                  <div
                    key={a.id}
                    className={`card ${a.available ? "" : "dim"}`}
                  >
                    <div className="itemTop">
                      <div className="stack">
                        <strong>{a.name}</strong>
                        <span className="muted">
                          {a.species} — {a.city}/{a.state}
                        </span>

                        <div className="row">
                          <span
                            className={`badge ${
                              a.available ? "success" : "danger"
                            }`}
                          >
                            {a.available ? "Disponível" : "Já adotado"}
                          </span>

                          <span className="badge warn">
                            Solicitações: {animalReqs.length} (Pendentes:{" "}
                            {pending.length})
                          </span>
                        </div>
                      </div>

                      <div className="actions">
                        {a.available ? (
                          <button
                            className="btn danger"
                            disabled={actingId === `animal-${a.id}`}
                            onClick={() =>
                              setAnimalAvailability(a.id, false)
                            }
                          >
                            {actingId === `animal-${a.id}`
                              ? "Atualizando..."
                              : "Marcar como adotado"}
                          </button>
                        ) : (
                          <button
                            className="btn success"
                            disabled={actingId === `animal-${a.id}`}
                            onClick={() =>
                              setAnimalAvailability(a.id, true)
                            }
                          >
                            {actingId === `animal-${a.id}`
                              ? "Atualizando..."
                              : "Reabrir para adoção"}
                          </button>
                        )}
                      </div>
                    </div>

                    {/* ===== Pendentes ===== */}
                    {pending.length > 0 && (
                      <div style={{ marginTop: 12 }}>
                        <div className="row" style={{ marginBottom: 8 }}>
                          <strong>📌 Pendentes</strong>
                          <span className="hint">
                            Aprove ou rejeite as solicitações
                          </span>
                        </div>

                        <div className="list">
                          {pending.map((r) => (
                            <div
                              key={r.id}
                              className="card dim warnOutline"
                            >
                              <div className="stack">
                                <div className="row">
                                  <strong>Pedido #{r.id}</strong>
                                  <span className="badge warn">
                                    {(r.status || "PENDENTE").toUpperCase()}
                                  </span>
                                </div>

                                <span className="muted">
                                  Adotante (user_id): <b>{r.user_id}</b>
                                </span>

                                {r.message && (
                                  <span className="muted">
                                    “{r.message}”
                                  </span>
                                )}

                                <div className="actions">
                                  <button
                                    className="btn success"
                                    disabled={actingId === r.id}
                                    onClick={() =>
                                      setRequestStatus(r.id, "APROVADO")
                                    }
                                  >
                                    {actingId === r.id
                                      ? "Processando..."
                                      : "✅ Aprovar"}
                                  </button>

                                  <button
                                    className="btn danger"
                                    disabled={actingId === r.id}
                                    onClick={() =>
                                      setRequestStatus(r.id, "REJEITADO")
                                    }
                                  >
                                    {actingId === r.id
                                      ? "Processando..."
                                      : "❌ Rejeitar"}
                                  </button>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* ===== Histórico completo ===== */}
                    {animalReqs.length > 0 && (
                      <div style={{ marginTop: 12 }}>
                        <details>
                          <summary style={{ cursor: "pointer" }}>
                            Ver histórico completo
                          </summary>

                          <div className="list" style={{ marginTop: 10 }}>
                            {animalReqs.map((r) => {
                              const s = (r.status || "").toUpperCase();
                              return (
                                <div
                                  key={r.id}
                                  className={`card dim ${
                                    s === "APROVADO"
                                      ? "successOutline"
                                      : s === "REJEITADO"
                                      ? "dangerOutline"
                                      : "warnOutline"
                                  }`}
                                >
                                  <div className="stack">
                                    <div className="row">
                                      <strong>#{r.id}</strong>
                                      <span className="badge warn">
                                        {s}
                                      </span>
                                      <span className="muted">
                                        user_id: <b>{r.user_id}</b>
                                      </span>
                                    </div>

                                    {r.message && (
                                      <span className="muted">
                                        “{r.message}”
                                      </span>
                                    )}
                                  </div>
                                </div>
                              );
                            })}
                          </div>
                        </details>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}

          <hr />

          <h2 className="sectionTitle">📌 Todas as solicitações</h2>

          {requests.length === 0 ? (
            <div className="card">
              <p className="muted" style={{ margin: 0 }}>
                Nenhuma solicitação encontrada.
              </p>
            </div>
          ) : (
            <div className="list">
              {requests
                .slice()
                .sort((a, b) => (b.id || 0) - (a.id || 0))
                .map((r) => {
                  const s = (r.status || "").toUpperCase();
                  return (
                    <div
                      key={r.id}
                      className={`card dim ${
                        s === "APROVADO"
                          ? "successOutline"
                          : s === "REJEITADO"
                          ? "dangerOutline"
                          : "warnOutline"
                      }`}
                    >
                      <div className="stack">
                        <div className="row">
                          <strong>#{r.id}</strong>
                          <span className="badge warn">{s}</span>
                        </div>

                        <span className="muted">
                          Animal: <b>{r.animal_id}</b> — Adotante (user_id):{" "}
                          <b>{r.user_id}</b>
                        </span>

                        {r.message && (
                          <span className="muted">“{r.message}”</span>
                        )}
                      </div>
                    </div>
                  );
                })}
            </div>
          )}
        </>
      )}
    </DashboardShell>
  );

}
