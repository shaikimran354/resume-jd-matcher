import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [resume, setResume] = useState(null);
  const [jdText, setJdText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (!resume || !jdText.trim()) {
      setError("Please upload a resume and enter a job description.");
      return;
    }
    setError("");
    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("jd_text", jdText);

    try {
      const res = await axios.post("https://praveen5001-resume-jd-matcher.hf.space/match", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(res.data);
    } catch (err) {
      setError("Something went wrong. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return "#22c55e";
    if (score >= 60) return "#f59e0b";
    if (score >= 40) return "#f97316";
    return "#ef4444";
  };

  return (
    <div className="app">
      <header className="header">
        <h1>🎯 AI Resume-JD Matcher</h1>
        <p>Upload your resume and paste a job description to see how well you match</p>
      </header>

      <div className="container">
        <div className="card">
          <h2>📄 Upload Resume</h2>
          <input
            type="file"
            accept=".pdf,.docx,.txt"
            onChange={(e) => setResume(e.target.files[0])}
            className="file-input"
          />
          {resume && <p className="file-name">✅ {resume.name}</p>}
        </div>

        <div className="card">
          <h2>📋 Job Description</h2>
          <textarea
            rows={10}
            placeholder="Paste the job description here..."
            value={jdText}
            onChange={(e) => setJdText(e.target.value)}
            className="textarea"
          />
        </div>

        {error && <p className="error">{error}</p>}

        <button onClick={handleSubmit} disabled={loading} className="btn">
          {loading ? "Analyzing..." : "🔍 Match Resume"}
        </button>

        {result && (
          <div className="results">
            <div className="score-card">
              <h2>Match Score</h2>
              <div
                className="score-circle"
                style={{ borderColor: getScoreColor(result.score) }}
              >
                <span style={{ color: getScoreColor(result.score) }}>
                  {result.score}%
                </span>
              </div>
            </div>

            <div className="feedback-card">
              <h2>💡 Feedback</h2>
              {result.feedback.map((f, i) => (
                <p key={i} className="feedback-item">• {f}</p>
              ))}
            </div>

            <div className="keywords-grid">
              <div className="keyword-card green">
                <h3>✅ Matching Keywords ({result.common_keywords.length})</h3>
                <div className="tags">
                  {result.common_keywords.slice(0, 20).map((k, i) => (
                    <span key={i} className="tag green-tag">{k}</span>
                  ))}
                </div>
              </div>

              <div className="keyword-card red">
                <h3>❌ Missing Keywords ({result.missing_keywords.length})</h3>
                <div className="tags">
                  {result.missing_keywords.slice(0, 20).map((k, i) => (
                    <span key={i} className="tag red-tag">{k}</span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;