export default function Notes({ data }) {
  return (
    <div className="notes">
      <h3>{data.title}</h3>
      <p className="summary">{data.summary}</p>
      {(data.sections || []).map((s, i) => (
        <section key={i}>
          <h4>{s.heading}</h4>
          <ul>{s.points.map((p, j) => <li key={j}>{p}</li>)}</ul>
        </section>
      ))}
      {data.key_terms?.length > 0 && (
        <>
          <h4>Key terms</h4>
          <div className="terms">
            {data.key_terms.map((t, i) => (
              <div key={i} className="term"><b>{t.term}</b><span>{t.definition}</span></div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
