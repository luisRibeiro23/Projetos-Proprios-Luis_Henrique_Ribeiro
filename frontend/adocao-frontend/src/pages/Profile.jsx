import { useEffect, useState } from "react";
import { api } from "../services/api";

export default function Profile() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    api("/auth/me").then(setUser);
  }, []);

  if (!user) return <p className="muted">Carregando...</p>;

  return (
    <div className="container">
      <h1>Meu perfil</h1>

      <div className="card" style={{ marginTop: 16 }}>
        <p><b>Nome:</b> {user.name}</p>
        <p><b>Email:</b> {user.email}</p>
        <p><b>Tipo:</b> {user.role}</p>
        <p><b>Local:</b> {user.city}/{user.state}</p>
      </div>
    </div>
  );
}
