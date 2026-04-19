import React, { useState } from "react";
import { createRoot } from "react-dom/client";

type Citation = {
  doc_id: string;
  chunk_id: number;
  score: number;
};

type ChatResponse = {
  answer: string;
  citations: Citation[];
  disclaimer: string;
};

function App() {
  const [message, setMessage] = useState("");
  const [jurisdiction, setJurisdiction] = useState("US");
  const [practiceArea, setPracticeArea] = useState("general");
  const [response, setResponse] = useState<ChatResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const submit = async () => {
    if (!message.trim()) return;
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message,
          jurisdiction,
          practice_area: practiceArea,
        }),
      });
      const data = (await res.json()) as ChatResponse;
      setResponse(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={{ maxWidth: 850, margin: "2rem auto", fontFamily: "Arial, sans-serif" }}>
      <h1>Legal Advisor Chatbot</h1>
      <p>Educational assistant with retrieval grounding and citations.</p>

      <div style={{ display: "grid", gap: 12, marginTop: 18 }}>
        <label>
          Jurisdiction
          <input value={jurisdiction} onChange={(e) => setJurisdiction(e.target.value)} />
        </label>

        <label>
          Practice Area
          <input value={practiceArea} onChange={(e) => setPracticeArea(e.target.value)} />
        </label>

        <label>
          Ask a legal question
          <textarea
            rows={5}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Example: What are key requirements for a valid contract?"
          />
        </label>

        <button onClick={submit} disabled={loading}>
          {loading ? "Thinking..." : "Send"}
        </button>
      </div>

      {response && (
        <section style={{ marginTop: 24 }}>
          <h2>Answer</h2>
          <pre style={{ whiteSpace: "pre-wrap" }}>{response.answer}</pre>

          <h3>Citations</h3>
          <ul>
            {response.citations.map((c, i) => (
              <li key={`${c.doc_id}-${i}`}>
                {c.doc_id} / chunk {c.chunk_id} / score {c.score.toFixed(3)}
              </li>
            ))}
          </ul>

          <p style={{ borderLeft: "4px solid #f39c12", paddingLeft: 12 }}>{response.disclaimer}</p>
        </section>
      )}
    </main>
  );
}

createRoot(document.getElementById("root")!).render(<App />);
