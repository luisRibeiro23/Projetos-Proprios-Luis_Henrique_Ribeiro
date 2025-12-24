import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import "../styles/auth.css";
import { api } from "../services/api";

export default function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    setErr(null);

    if (!email || !password) {
      setErr("Preencha e-mail e senha.");
      return;
    }

    try {
      setLoading(true);

      // 1) chama login
      const data = await api("/auth/login", {
        method: "POST",
        body: { email, password },
      });

      // 🔎 DEBUG: veja no console o que está vindo do backend
      console.log("LOGIN RESPONSE:", data);

      // 2) tenta extrair token e user em formatos diferentes
      const token =
        data?.token ||
        data?.access_token ||
        data?.jwt ||
        data?.data?.token ||
        data?.data?.access_token;

      let user =
        data?.user ||
        data?.currentUser ||
        data?.usuario ||
        data?.data?.user ||
        data?.data?.currentUser;

      if (!token) {
        throw new Error("Login OK, mas não veio token na resposta.");
      }

      // 3) salva token
      localStorage.setItem("token", token);

      // 4) se não veio user no login, tenta buscar /auth/me
      if (!user) {
        try {
          const me = await api("/auth/me");
          console.log("AUTH ME RESPONSE:", me);
          user = me;
        } catch (e) {
          // Se seu backend não tem /auth/me, você vai cair aqui
          // Nesse caso, o sistema ainda terá token salvo, mas sem user.
          console.warn("Não foi possível buscar /auth/me:", e.message);
        }
      }

      if (!user) {
        // evita deixar token salvo sem user (estado inconsistente)
        localStorage.removeItem("token");
        localStorage.removeItem("currentUser");
        throw new Error(
          "Login funcionou, mas não foi possível obter os dados do usuário (user)."
        );
      }

      // 5) salva user
      localStorage.setItem("currentUser", JSON.stringify(user));

      // 🔎 DEBUG: confirma que salvou
      console.log("SAVED token:", localStorage.getItem("token"));
      console.log("SAVED currentUser:", localStorage.getItem("currentUser"));

      // 6) vai pra Home
      navigate("/");
    } catch (e) {
      setErr(e.message || "Falha ao logar.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-header">
          <h1
          className="auth-title"
          style={{ color: "#2f3bd6" }}
          >
            Entrar
            </h1>
          <p className="auth-subtitle">Acesse sua conta no AdoCÃO 🐶</p>
        </div>

        {err && <div className="alert alert-error">{err}</div>}

        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="form-row">
            <label>E-mail</label>
            <input
              className="input"
              type="email"
              placeholder="seuemail@exemplo.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="form-row">
            <label>Senha</label>
            <input
              className="input"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button
          className="auth-submit"
          disabled={loading}
          style={{ color: "#5b67f4" }}
          >
            {loading ? "Entrando..." : "Entrar"}
          </button>
        </form>

        <div className="divider" />

        <div
        className="auth-footer"
        style={{ color: "#444" }}>
          Não tem conta?{" "}
          <Link className="link" to="/register">
            Criar conta
          </Link>
        </div>
      </div>
    </div>
  );
}
