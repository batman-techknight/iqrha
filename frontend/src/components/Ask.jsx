import { useState } from "react";
import { ask } from "../api";

export default function Ask({ docId }) {
  const [msgs, setMsgs] = useState([]);
  const [q, setQ] = useState("");
  const [busy, setBusy] = useState(false);

  async function send(e) {
    e.preventDefault();
    if (!q.trim() || busy) return;
    const question = q;
    setQ("");
    setMsgs((m) => [...m, { role: "user", text: question }]);
    setBusy(true);
    try {
      const r = await ask(docId, question);
      setMsgs((m) => [...m, { role: "ai", text: r.answer }]);
    } catch (err) {
      setMsgs((m) => [...m, { role: "ai", text: "⚠️ " + err.message }]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="chat">
      <div className="msgs">
        {!msgs.length && <p className="muted">Ask anything about this document, e.g. “Explain the main idea simply.”</p>}
        {msgs.map((m, i) => <div key={i} className={`msg ${m.role}`}>{m.text}</div>)}
        {busy && <div className="msg ai">Thinking…</div>}
      </div>
      <form onSubmit={send}>
        <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Ask a question…" />
        <button className="btn" disabled={busy}>Send</button>
      </form>
    </div>
  );
}
