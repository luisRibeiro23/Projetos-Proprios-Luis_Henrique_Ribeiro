import { useEffect, useState } from "react";

type AdoptionStatus = "PENDENTE" | "APROVADO" | "RECUSADO";

interface AdoptionRequest {
  id: number;
  animal_id: number;
  message: string | null;
  status: AdoptionStatus;
  created_at: string;
  updated_at?: string;
}

const API_URL = "http://127.0.0.1:8000";

export function MyAdoptions() {
  const [requests, setRequests] = useState<AdoptionRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // aqui supõe que você salva o token no localStorage ao logar
  const token = localStorage.getItem("token");

  useEffect(() => {
    async function fetchRequests() {
      try {
        setLoading(true);
        setError(null);

        const res = await fetch(`${API_URL}/adoption-requests/me`, {
          headers: {
            "Content-Type": "application/json",
            Authorization: token ? `Bearer ${token}` : "",
          },
        });

        if (!res.ok) {
          throw new Error(`Erro ao carregar solicitações: ${res.status}`);
        }

        const data: AdoptionRequest[] = await res.json();
        setRequests(data);
      } catch (err: any) {
        setError(err.message ?? "Erro ao carregar solicitações");
      } finally {
        setLoading(false);
      }
    }

    if (token) {
      fetchRequests();
    } else {
      setError("Você precisa estar logado para ver suas solicitações.");
      setLoading(false);
    }
  }, [token]);

  if (loading) {
    return <p>Carregando suas solicitações...</p>;
  }

  if (error) {
    return <p style={{ color: "red" }}>{error}</p>;
  }

  if (requests.length === 0) {
    return <p>Você ainda não fez nenhuma solicitação de adoção.</p>;
  }

  return (
    <div style={{ maxWidth: 800, margin: "0 auto" }}>
      <h2>Minhas solicitações de adoção</h2>
      <table style={{ width: "100%", borderCollapse: "collapse", marginTop: 16 }}>
        <thead>
          <tr>
            <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>ID</th>
            <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>Animal</th>
            <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>Mensagem</th>
            <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>Status</th>
            <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>Data</th>
          </tr>
        </thead>
        <tbody>
          {requests.map((req) => (
            <tr key={req.id}>
              <td style={{ borderBottom: "1px solid #eee" }}>{req.id}</td>
              <td style={{ borderBottom: "1px solid #eee" }}>{req.animal_id}</td>
              <td style={{ borderBottom: "1px solid #eee" }}>
                {req.message || "-"}
              </td>
              <td style={{ borderBottom: "1px solid #eee" }}>
                {req.status === "PENDENTE" && "⏳ Pendente"}
                {req.status === "APROVADO" && "✅ Aprovado"}
                {req.status === "RECUSADO" && "❌ Recusado"}
              </td>
              <td style={{ borderBottom: "1px solid #eee" }}>
                {new Date(req.created_at).toLocaleString("pt-BR")}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
