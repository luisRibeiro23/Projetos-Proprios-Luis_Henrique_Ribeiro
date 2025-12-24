import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styles/auth.css";
import { api } from "../services/api";

export default function Register() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("ADOTANTE");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState(null);
  const [ok, setOk] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    setErr(null);
    setOk(null);

    if (!name || !email || !password) {
      setErr("Preencha nome, e-mail e senha.");
      return;
    }

    try {
      setLoading(true);

      // Ajuste conforme seu backend:
      // ex: POST /auth/register
      await api("/auth/register", {
        method: "POST",
        body: JSON.stringify({ name, email, password, role }),
      });

      setOk("Conta criada! Agora faça login.");
      // se preferir ir direto pro login:
      setTimeout(() => navigate("/login"), 800);
    } catch (e) {
      setErr(e.message || "Falha ao cadastrar.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-header">
          <h1 className="auth-title" >Criar conta</h1>
          <p className="auth-subtitle">Cadastre-se para adotar, doar ou atuar como ONG</p>
        </div>

        {err && <div className="alert alert-error">{err}</div>}
        {ok && <div className="alert alert-success">{ok}</div>}

        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="form-row">
            <label>Nome</label>
            <input
              className="input"
              placeholder="Seu nome"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>

          <div className="form-row">
            <label>E-mail</label>
            <input
              className="input"
              type="email"
              placeholder="seuemail@exemplo.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="form-row">
            <label>Tipo de usuário</label>
            <select
              className="select"
              value={role}
              onChange={(e) => setRole(e.target.value)}
            >
              <option value="ADOTANTE">Adotante</option>
              <option value="ONG">ONG</option>
              <option value="DOADOR">Doador</option>
            </select>
          </div>

          <div className="form-row">
            <label>Senha</label>
            <input
              className="input"
              type="password"
              placeholder="Crie uma senha"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button className="btn-primary" disabled={loading} style={{ color: "#5b67f4" }}>
            {loading ? "Cadastrando..." : "Criar conta"}
          </button>
        </form>

        <div className="divider" />

        <div className="auth-footer" style={{ color: "#444" }}>
          Já tem conta? <Link className="link" to="/login">Entrar</Link>
        </div>
      </div>
    </div>
  );
}
