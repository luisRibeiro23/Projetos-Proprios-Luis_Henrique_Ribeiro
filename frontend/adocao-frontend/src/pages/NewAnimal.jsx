import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../services/api";

export default function NewAnimal() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("currentUser") || "null");

  const [name, setName] = useState("");
  const [species, setSpecies] = useState("Cachorro");
  const [size, setSize] = useState("MEDIO");

  const [age, setAge] = useState("");
  const [ageUnit, setAgeUnit] = useState("ANOS");

  const [description, setDescription] = useState("");

  const [city, setCity] = useState("Manaus");
  const [stateUF, setStateUF] = useState("AM");

  // ✅ multi imagens
  const [imageFiles, setImageFiles] = useState([]);       // File[]
  const [imagePreviews, setImagePreviews] = useState([]); // string[]

  const [creating, setCreating] = useState(false);
  const fileRef = useRef(null);

  useEffect(() => {
    if (!user) navigate("/login");
    else if (user.role !== "ONG") navigate("/dashboard");
  }, [navigate]); // user não precisa, porque vem do localStorage

  function pickImage() {
    fileRef.current?.click();
  }

  function onFileChange(e) {
    const files = Array.from(e.target.files || []);
    if (!files.length) return;

    const toAddFiles = [];
    const toAddPreviews = [];

    for (const file of files) {
      if (!file.type.startsWith("image/")) continue;
      if (file.size > 5 * 1024 * 1024) continue;

      // evita duplicar (mesmo arquivo selecionado de novo)
      const already = imageFiles.some(
        (f) => f.name === file.name && f.size === file.size
      );
      if (already) continue;

      toAddFiles.push(file);
      toAddPreviews.push(URL.createObjectURL(file));
    }

    if (!toAddFiles.length) {
      alert("Nada novo para adicionar (ou arquivos inválidos/duplicados).");
      if (fileRef.current) fileRef.current.value = "";
      return;
    }

    setImageFiles((prev) => [...prev, ...toAddFiles]);
    setImagePreviews((prev) => [...prev, ...toAddPreviews]);

    // permite selecionar o mesmo arquivo novamente no futuro (se remover e quiser re-adicionar)
    if (fileRef.current) fileRef.current.value = "";
  }


  function cleanupPreviews() {
    for (const url of imagePreviews) {
      try {
        URL.revokeObjectURL(url);
      } catch {}
    }
  }

  function removeAllImages() {
    cleanupPreviews();
    setImageFiles([]);
    setImagePreviews([]);
    if (fileRef.current) fileRef.current.value = "";
  }

  function removeOneImage(index) {
    const url = imagePreviews[index];
    if (url) URL.revokeObjectURL(url);

    setImageFiles((prev) => prev.filter((_, i) => i !== index));
    setImagePreviews((prev) => prev.filter((_, i) => i !== index));
  }

  useEffect(() => {
    // cleanup quando desmontar
    return () => cleanupPreviews();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function createAnimal(e) {
    e.preventDefault();

    if (!name.trim()) return alert("Informe o nome.");
    if (!species.trim()) return alert("Informe a espécie.");
    if (!size) return alert("Informe o porte.");
    if (!city.trim()) return alert("Informe a cidade.");

    const uf = (stateUF || "").trim().toUpperCase();
    if (uf.length !== 2) return alert("UF deve ter 2 letras (ex: AM).");

    if (age !== "" && Number(age) < 0) return alert("Idade não pode ser negativa.");

    let ageToSend = "";
    if (age !== "") {
      const n = Number(age);
      ageToSend = String(ageUnit === "MESES" ? Math.round((n / 12) * 10) / 10 : n);
    }

    try {
      setCreating(true);

      // 1) cria animal (SEM foto principal aqui)
      const fd = new FormData();
      fd.append("name", name.trim());
      fd.append("species", species.trim());
      fd.append("size", size);
      if (age !== "") fd.append("age", ageToSend);
      fd.append("city", city.trim());
      fd.append("state", uf);
      if (description.trim()) fd.append("description", description.trim());

      const created = await api("/animals", {
        method: "POST",
        body: fd,
      });

      const animalId = created?.id;
      if (!animalId) {
        throw new Error("Animal criado, mas não retornou ID.");
      }

      // 2) se tiver fotos, envia todas no endpoint /photos
      if (imageFiles.length) {
        const fdPhotos = new FormData();
        for (const f of imageFiles) fdPhotos.append("files", f);

        await api(`/animals/${animalId}/photos`, {
          method: "POST",
          body: fdPhotos,
        });
      }

      alert("Animal cadastrado com sucesso!");
      navigate("/dashboard/ong");
      // se preferir ir pro perfil:
      // navigate(`/animals/${animalId}`);
    } catch (err) {
      alert("Erro ao criar animal: " + (err.message || "erro"));
    } finally {
      setCreating(false);
    }
  }

  return (
    <div className="container">
      <div className="header">
        <div>
          <div className="brand">
            <div style={{ fontSize: 34 }}>➕</div>
            <h1>Novo animal</h1>
          </div>
          <p className="subtitle">Cadastre um animal para adoção</p>
        </div>

        <div className="actions">
          <button className="btn" onClick={() => navigate("/dashboard/ong")}>
            ← Voltar
          </button>
          <button className="btn" onClick={() => navigate("/")}>
            Home
          </button>
        </div>
      </div>

      <hr className="divider" />

      <div className="card">
        <form onSubmit={createAnimal} className="stack" style={{ gap: 12 }}>
          {/* Upload imagens */}
          <div className="stack">
            <label className="label">Fotos do animal (opcional)</label>

            <input
              ref={fileRef}
              type="file"
              accept="image/*"
              multiple
              onChange={onFileChange}
              style={{ display: "none" }}
            />

            <div
              onClick={pickImage}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => (e.key === "Enter" ? pickImage() : null)}
              style={{
                border: "2px dashed rgba(255,255,255,0.25)",
                borderRadius: 14,
                padding: 16,
                cursor: "pointer",
                background: "rgba(255,255,255,0.04)",
                display: "flex",
                alignItems: "center",
                gap: 14,
              }}
            >
              <div
                style={{
                  width: 64,
                  height: 64,
                  borderRadius: 12,
                  background: "rgba(255,255,255,0.08)",
                  display: "grid",
                  placeItems: "center",
                  fontSize: 26,
                }}
              >
                +
              </div>

              <div style={{ flex: 1 }}>
                <strong>Adicionar imagens</strong>
                <div className="muted" style={{ marginTop: 4 }}>
                  Clique para escolher (até 5MB cada)
                </div>
              </div>
            </div>

            {!!imagePreviews.length && (
              <div style={{ marginTop: 12 }}>
                <div className="row" style={{ justifyContent: "space-between" }}>
                  <strong>Preview ({imagePreviews.length})</strong>
                  <button type="button" className="btn danger" onClick={removeAllImages}>
                    Remover todas
                  </button>
                </div>

                <div
                  style={{
                    marginTop: 10,
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fill, minmax(110px, 1fr))",
                    gap: 10,
                  }}
                >
                  {imagePreviews.map((src, i) => (
                    <div key={src} style={{ position: "relative" }}>
                      <img
                        src={src}
                        alt={`Preview ${i + 1}`}
                        style={{
                          width: "100%",
                          height: 110,
                          objectFit: "cover",
                          borderRadius: 12,
                        }}
                      />
                      <button
                        type="button"
                        className="btn danger"
                        onClick={() => removeOneImage(i)}
                        style={{
                          position: "absolute",
                          right: 6,
                          top: 6,
                          padding: "6px 8px",
                          fontSize: 12,
                        }}
                        aria-label="Remover imagem"
                      >
                        ✖
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="grid2">
            <div className="stack">
              <label className="label">Nome</label>
              <input
                className="input"
                placeholder="Ex: Thor"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>

            <div className="stack">
              <label className="label">Espécie</label>
              <input
                className="input"
                placeholder="Ex: Cachorro"
                value={species}
                onChange={(e) => setSpecies(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="grid2">
            <div className="stack">
              <label className="label">Porte</label>
              <select className="input" value={size} onChange={(e) => setSize(e.target.value)}>
                <option value="PEQUENO">Pequeno</option>
                <option value="MEDIO">Médio</option>
                <option value="GRANDE">Grande</option>
              </select>
            </div>

            <div className="stack">
              <label className="label">Idade</label>
              <div className="row" style={{ gap: 8 }}>
                <input
                  className="input"
                  type="number"
                  min={0}
                  placeholder={ageUnit === "MESES" ? "Meses" : "Anos"}
                  value={age}
                  onChange={(e) => setAge(e.target.value)}
                  style={{ flex: 1 }}
                />
                <select
                  className="input"
                  value={ageUnit}
                  onChange={(e) => setAgeUnit(e.target.value)}
                  style={{ width: 140 }}
                >
                  <option value="ANOS">Anos</option>
                  <option value="MESES">Meses</option>
                </select>
              </div>
            </div>
          </div>

          <div className="stack">
            <label className="label">Descrição</label>
            <textarea
              className="input"
              rows={4}
              placeholder="Temperamento, vacinas, cuidados, etc."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>

          <div className="grid2">
            <div className="stack">
              <label className="label">Cidade</label>
              <input
                className="input"
                placeholder="Cidade"
                value={city}
                onChange={(e) => setCity(e.target.value)}
                required
              />
            </div>

            <div className="stack">
              <label className="label">UF</label>
              <input
                className="input"
                placeholder="AM"
                value={stateUF}
                onChange={(e) => setStateUF(e.target.value.toUpperCase())}
                required
                maxLength={2}
              />
            </div>
          </div>

          <div className="row" style={{ justifyContent: "flex-end", gap: 8 }}>
            <button className="btn" type="button" onClick={() => navigate("/dashboard/ong")}>
              Cancelar
            </button>

            <button className="btn btn-primary" type="submit" disabled={creating}>
              {creating ? "Cadastrando..." : "Cadastrar"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
