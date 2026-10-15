const BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function req(path, opts = {}) {
  const r = await fetch(BASE + path, opts);
  if (!r.ok) {
    const e = await r.json().catch(() => ({}));
    throw new Error(e.detail || "Request failed");
  }
  return r.json();
}

export const listDocs = () => req("/api/documents");

export const upload = (file) => {
  const f = new FormData();
  f.append("file", file);
  return req("/api/documents", { method: "POST", body: f });
};

export const getOutput = (id, kind) => req(`/api/documents/${id}/outputs/${kind}`);

export const generate = (id, kind, count = 10) =>
  req(`/api/documents/${id}/generate/${kind}?count=${count}`, { method: "POST" });

export const ask = (id, question) =>
  req(`/api/documents/${id}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
