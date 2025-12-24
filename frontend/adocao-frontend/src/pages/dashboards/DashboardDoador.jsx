import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import DashboardShell from "../../components/DashboardShell";


export default function DashboardDoador() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("currentUser") || "null");

  useEffect(() => {
    if (!user) navigate("/login");
    if (user?.role !== "DOADOR") navigate("/dashboard");
  }, [user, navigate]);

  return (
    <DashboardShell
      title="💙 Dashboard do Doador"
      subtitle={
        <>
          Logado como: <b>{user?.name}</b>
        </>
      }
      actions={
        <>
          <button className="btn" onClick={() => navigate("/")}>Home</button>
          <button
            className="btn danger"
            onClick={() => {
              localStorage.removeItem("token");
              localStorage.removeItem("currentUser");
              navigate("/login");
            }}
          >
            Sair
          </button>
        </>
      }
    >
      <div className="statsGrid">
        <div className="card">
          <div className="kv">
            <strong>Doações realizadas</strong>
            <span>Em breve</span>
          </div>
        </div>

        <div className="card">
          <div className="kv">
            <strong>ONGs apoiadas</strong>
            <span>Em breve</span>
          </div>
        </div>

        <div className="card">
          <div className="kv">
            <strong>Última contribuição</strong>
            <span>Em breve</span>
          </div>
        </div>
      </div>

      <hr />

      <h2 className="sectionTitle">📌 Histórico</h2>
      <div className="card">
        <p className="muted" style={{ margin: 0 }}>
          Aqui você verá suas contribuições (pix, ração, medicamentos etc.).
        </p>
      </div>
    </DashboardShell>
  );


}
