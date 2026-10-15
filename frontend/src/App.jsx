import { useEffect, useRef, useState } from "react";
import { listDocs, upload } from "./api";
import { useOutput } from "./useOutput";
import Notes from "./components/Notes";
import Flashcards from "./components/Flashcards";
import Quiz from "./components/Quiz";
import Ask from "./components/Ask";

const TABS = [
  ["notes", "📝 Notes"],
  ["flashcards", "🃏 Flashcards"],
  ["quiz", "🎯 Final Quiz"],
  ["ask", "💬 Ask"],
];

function Section({ docId, kind, label, withCount, render }) {
  const { data, loading, error, run, version } = useOutput(docId, kind);
  const [count, setCount] = useState(10);
  return (
    <div>
      <div className="toolbar">
        {withCount && (
          <select value={count} onChange={(e) => setCount(+e.target.value)}>
            {[5, 10, 15, 20].map((n) => (
              <option key={n} value={n}>{n} items</option>
            ))}
          </select>
        )}
        <button className="btn" onClick={() => run(count)} disabled={loading}>
          {loading ? "Generating…" : data ? `Regenerate ${label}` : `Generate ${label}`}
        </button>
      </div>
      {error && <p className="error">{error}</p>}
      {loading && <div className="skeleton" />}
      {!loading && data && <div key={version}>{render(data)}</div>}
      {!loading && !data && !error && (
        <p className="muted">Nothing here yet. Hit generate to create your {label.toLowerCase()}.</p>
      )}
    </div>
  );
}

export default function App() {
  const [docs, setDocs] = useState([]);
  const [active, setActive] = useState(null);
  const [tab, setTab] = useState("notes");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [drag, setDrag] = useState(false);
  const input = useRef();

  useEffect(() => {
    listDocs()
      .then((d) => {
        setDocs(d);
        if (d[0]) setActive(d[0].id);
      })
      .catch(() => setError("Can't reach the server. Is the backend running?"));
  }, []);

  async function handleFile(file) {
    if (!file) return;
    setBusy(true);
    setError("");
    try {
      const doc = await upload(file);
      setDocs((d) => [{ ...doc }, ...d]);
      setActive(doc.id);
      setTab("notes");
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }

  const doc = docs.find((d) => d.id === active);

  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="logo">IQRHA<span>.</span></div>
        <p className="tag">Your personal AI study assistant</p>

        <div
          className={`drop ${drag ? "drag" : ""}`}
          onClick={() => input.current.click()}
          onDragOver={(e) => { e.preventDefault(); setDrag(true); }}
          onDragLeave={() => setDrag(false)}
          onDrop={(e) => { e.preventDefault(); setDrag(false); handleFile(e.dataTransfer.files[0]); }}
        >
          <div className="drop-icon">{busy ? "⏳" : "📄"}</div>
          <strong>{busy ? "Reading your file…" : "Upload study material"}</strong>
          <small>PDF · DOCX · TXT · MD (max 10 MB)</small>
          <input ref={input} type="file" hidden accept=".pdf,.docx,.txt,.md"
                 onChange={(e) => handleFile(e.target.files[0])} />
        </div>
        {error && <p className="error">{error}</p>}

        <h4>Your files</h4>
        <ul className="docs">
          {docs.map((d) => (
            <li key={d.id} className={d.id === active ? "on" : ""} onClick={() => setActive(d.id)}>
              {d.name}
            </li>
          ))}
          {!docs.length && <li className="muted">No files yet</li>}
        </ul>
      </aside>

      <main className="main">
        {!doc ? (
          <div className="hero">
            <h1>Learn faster from <em>your own</em> notes.</h1>
            <p>Upload a file and IQRHA turns it into simple notes, flashcards and a final-test quiz.</p>
          </div>
        ) : (
          <>
            <h2 className="doc-title">{doc.name}</h2>
            <nav className="tabs">
              {TABS.map(([k, label]) => (
                <button key={k} className={tab === k ? "on" : ""} onClick={() => setTab(k)}>{label}</button>
              ))}
            </nav>
            <div className="panel">
              {tab === "notes" && (
                <Section docId={doc.id} kind="notes" label="Notes" render={(d) => <Notes data={d} />} />
              )}
              {tab === "flashcards" && (
                <Section docId={doc.id} kind="flashcards" label="Flashcards" withCount
                         render={(d) => <Flashcards cards={d.cards || []} />} />
              )}
              {tab === "quiz" && (
                <Section docId={doc.id} kind="quiz" label="Quiz" withCount
                         render={(d) => <Quiz questions={d.questions || []} />} />
              )}
              {tab === "ask" && <Ask key={doc.id} docId={doc.id} />}
            </div>
          </>
        )}
      </main>
    </div>
  );
}
