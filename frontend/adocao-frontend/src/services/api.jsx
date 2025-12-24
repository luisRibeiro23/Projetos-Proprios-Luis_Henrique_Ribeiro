// api.jsx
const BASE_URL = "http://127.0.0.1:8000";

export async function api(path, options = {}) {
  const token = localStorage.getItem("token");

  const headers = new Headers(options.headers || {});
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const body = options.body;

  const isFormData =
    typeof FormData !== "undefined" && body instanceof FormData;

  const isUrlEncoded =
    typeof URLSearchParams !== "undefined" && body instanceof URLSearchParams;

  // JSON "normal" (objeto plain)
  const isPlainObject =
    body &&
    typeof body === "object" &&
    !isFormData &&
    !isUrlEncoded &&
    !(body instanceof Blob);

  if (isPlainObject) {
    if (!headers.has("Content-Type")) headers.set("Content-Type", "application/json");
    options.body = JSON.stringify(body);
  }

  // URL encoded (não transformar em JSON)
  if (isUrlEncoded) {
    if (!headers.has("Content-Type"))
      headers.set("Content-Type", "application/x-www-form-urlencoded");
    // options.body já está ok
  }

  // Se for FormData, NÃO setar Content-Type
  if (isFormData) headers.delete("Content-Type");

  const res = await fetch(`${BASE_URL}${path}`, { ...options, headers });

  const contentType = res.headers.get("content-type") || "";
  const isJson = contentType.includes("application/json");
  const data = isJson ? await res.json().catch(() => null) : await res.text().catch(() => null);

  if (!res.ok) {
    const msg =
      (data && typeof data === "object" && (data.detail || data.message)) ||
      (typeof data === "string" && data) ||
      `Erro HTTP ${res.status}`;
    throw new Error(msg);
  }

  return data;
}
