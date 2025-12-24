import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api } from "../services/api";

export default function EditAnimal() {
  const navigate = useNavigate();
  const { id } = useParams();

  const user = JSON.parse(localStorage.getItem("currentUser") || "null");

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [err, setErr] = useState(null);

  // campos do form
  const [name, setName] = useState("");
  const [species, setSpecies] = useState("Cachorro");
  const [size, setSize] = useState("MEDIO");

  const [age, setAge] = useState("");       // string no input
  const [ageUnit, setAgeUnit] = useState("ANOS");

  const [city, setCity] = useState("Manaus");
  const [stateUF, setStateUF] = useState("AM");

  useEffect(() => {
    const u = JSON.parse(localStorage.getItem("currentUser") || "null");
    if (!u) navigate("/login");
    else if (u.role !== "ONG") navigate("/dashboard");
  }, [navigate]);

  // carregar dados do animal (usa /animals/:id e filtra por id como fallback)
  useEffect(() => {
    async function loadAnimal() {
      try {
        setLoading(true);
        setErr(null);

        let animal = null;

        // 1) tenta endpoint direto
        try {
          animal = await api(`/animals/${id}`);
        } catch (e) {
          // 2) fallback: pega meus animais e acha pelo id
          const mine = await api("/animals/me");
          animal = mine.find((a) => String(a.id) === String(id));
        }

        if (!animal) {
          setErr("Animal não encontrado (ou não pertence a esta ONG).");
          return;
        }

        setName(animal.name ?? "");
        setSpecies(animal.species ?? "");
        setSize(animal.size ?? "MEDIO");

        // age vem como string no seu backend (pelo erro 422 anterior)
        setAge(animal.age ?? "");
        setAgeUnit("ANOS"); // não temos unidade no backend, então assume ANOS

        setCity(animal.city ?? "");
        setStateUF(animal.state ?? "");
      } catch (e) {
        setErr(e.message || "Erro ao carregar animal.");
      } finally {
        setLoading(false);
      }
    }

    loadAnimal();
  }, [id]);

  async function handleSave(e) {
    e.preventDefault();

    try {
      setSaving(true);
      setErr(null);

      if (age !== "" && Number(age) < 0) {
        alert("Idade não pode ser negativa");
        return;
      }

      // se o usuário escolher MESES, converte para anos antes de enviar
      let ageToSend = null;
      if (age !== "") {
        const n = Number(age);
        const years = ageUnit === "MESES" ? Math.round((n / 12) * 10) / 10 : n;
        ageToSend = String(years); // backend quer string
      }

      await api(`/animals/${id}`, {
        method: "PATCH",
        body: JSON.stringify({
          name,
          species,
          size,
          age: ageToSend, // string ou null
          city,
          state: stateUF,
        }),
      });

      alert("Animal atualizado!");
      navigate("/dashboard/ong");
    } catch (e) {
      alert("Erro ao salvar: " + (e.message || e));
    } finally {
      setSaving(false);
    }
  }

  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("currentUser");
    navigate("/login");
  }

  if (loading) {
    return (
      <div style={{ padding: 20 }}>
        <h2>Editar animal</h2>
        <p>Carregando...</p>
      </div>
    );
  }

  return (
    <div style={{ padding: 20, maxWidth: 520 }}>
      <h2>Editar animal</h2>

      <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
        <button onClick={() => navigate("/dashboard/ong")}>← Voltar</button>
        <button onClick={logout}>Sair</button>
      </div>

      {err && <p style={{ color: "crimson" }}>Erro: {err}</p>}

      {!err && (
        <form onSubmit={handleSave}>
          <input
            placeholder="Nome"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          <br /><br />

          <input
            placeholder="Espécie (ex: Cachorro)"
            value={species}
            onChange={(e) => setSpecies(e.target.value)}
            required
          />
          <br /><br />

          <label>
            Porte:&nbsp;
            <select value={size} onChange={(e) => setSize(e.target.value)}>
              <option value="PEQUENO">Pequeno</option>
              <option value="MEDIO">Médio</option>
              <option value="GRANDE">Grande</option>
            </select>
          </label>
          <br /><br />

          <input
            type="number"
            min={0}
            placeholder={ageUnit === "MESES" ? "Idade em meses" : "Idade em anos"}
            value={age}
            onChange={(e) => setAge(e.target.value)}
          />

          <select value={ageUnit} onChange={(e) => setAgeUnit(e.target.value)}>
            <option value="ANOS">Anos</option>
            <option value="MESES">Meses</option>
          </select>
          <br /><br />

          <input
            placeholder="Cidade"
            value={city}
            onChange={(e) => setCity(e.target.value)}
            required
          />
          <br /><br />

          <input
            placeholder="UF (ex: AM)"
            value={stateUF}
            onChange={(e) => setStateUF(e.target.value.toUpperCase())}
            required
            maxLength={2}
          />
          <br /><br />

          <button type="submit" disabled={saving}>
            {saving ? "Salvando..." : "Salvar alterações"}
          </button>
        </form>
      )}
    </div>
  );
}
