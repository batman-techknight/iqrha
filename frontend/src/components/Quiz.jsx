import { useState } from "react";

export default function Quiz({ questions }) {
  const [i, setI] = useState(0);
  const [picked, setPicked] = useState(null);
  const [score, setScore] = useState(0);
  const [wrong, setWrong] = useState([]);
  const [done, setDone] = useState(false);

  if (!questions.length) return <p className="muted">No questions generated. Try again.</p>;
  const q = questions[i];

  const choose = (k) => {
    if (picked !== null) return;
    setPicked(k);
    if (k === q.answer) setScore((s) => s + 1);
    else setWrong((w) => [...w, { q, k }]);
  };
  const next = () => {
    if (i + 1 >= questions.length) setDone(true);
    else { setI(i + 1); setPicked(null); }
  };
  const restart = () => { setI(0); setPicked(null); setScore(0); setWrong([]); setDone(false); };

  if (done) {
    const pct = Math.round((score / questions.length) * 100);
    return (
      <div className="result">
        <div className="ring" style={{ "--p": pct }}><span>{pct}%</span></div>
        <h3>{pct >= 80 ? "Excellent work!" : pct >= 50 ? "Good effort, keep going!" : "Review and try again"}</h3>
        <p className="muted">You got {score} of {questions.length} correct.</p>
        {wrong.length > 0 && <h4>Review your mistakes</h4>}
        {wrong.map(({ q, k }, n) => (
          <div key={n} className="review">
            <b>{q.question}</b>
            <p className="bad">Your answer: {q.options[k]}</p>
            <p className="good">Correct: {q.options[q.answer]}</p>
            <small>{q.explanation}</small>
          </div>
        ))}
        <button className="btn" onClick={restart}>Retake quiz</button>
      </div>
    );
  }

  return (
    <div className="quiz">
      <div className="bar"><div style={{ width: `${(i / questions.length) * 100}%` }} /></div>
      <small className="muted">Question {i + 1} of {questions.length}</small>
      <h3>{q.question}</h3>
      {q.options.map((o, k) => {
        let cls = "opt";
        if (picked !== null) cls += k === q.answer ? " right" : k === picked ? " wrong" : "";
        return <button key={k} className={cls} onClick={() => choose(k)}>{o}</button>;
      })}
      {picked !== null && (
        <>
          <p className="explain">{q.explanation}</p>
          <button className="btn" onClick={next}>{i + 1 >= questions.length ? "Finish" : "Next"}</button>
        </>
      )}
    </div>
  );
}
