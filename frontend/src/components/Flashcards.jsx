import { useState } from "react";

export default function Flashcards({ cards }) {
  const [i, setI] = useState(0);
  const [flip, setFlip] = useState(false);
  if (!cards.length) return <p className="muted">No cards generated.</p>;

  const go = (d) => {
    setFlip(false);
    setI((i + d + cards.length) % cards.length);
  };
  const c = cards[i];

  return (
    <div className="fc">
      <div className={`card3d ${flip ? "flip" : ""}`} onClick={() => setFlip(!flip)}>
        <div className="face front"><small>Question</small><p>{c.front}</p></div>
        <div className="face back"><small>Answer</small><p>{c.back}</p></div>
      </div>
      <div className="fc-nav">
        <button className="btn ghost" onClick={() => go(-1)}>← Prev</button>
        <span>{i + 1} / {cards.length}</span>
        <button className="btn ghost" onClick={() => go(1)}>Next →</button>
      </div>
      <p className="muted center">Click the card to flip it</p>
    </div>
  );
}
