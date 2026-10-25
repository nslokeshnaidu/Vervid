import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function analyzeVideo() {
    if (!file) {
      setError("Please select a video first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Analysis failed.");
      }

      setResult(data.analysis);
    } catch (err) {
      setError(
        `${err.message} Make sure the VeriVid backend is running.`
      );
    } finally {
      setLoading(false);
    }
  }

  const report = result?.report;
  const verdictClass = (verdict) =>
    verdict?.toLowerCase() || "insufficient";

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <div className="brand-icon">V</div>
          <span>VeriVid</span>
        </div>
        <span className="header-tag">AI VIDEO FACT-CHECKER</span>
      </header>

      <main className="container">
        <section className="hero">
          <span className="eyebrow">VERIFY WHAT YOU WATCH</span>
          <h1>Separate facts from fiction.</h1>
          <p>
            Upload a video and let VeriVid extract factual claims,
            retrieve evidence, and evaluate each claim.
          </p>
        </section>

        <section className="upload-card">
          <div className="upload-heading">
            <div>
              <h2>Analyze a video</h2>
              <p>Choose a video file to begin fact-checking.</p>
            </div>
            <span className="step-number">01 / UPLOAD</span>
          </div>

          <label className="dropzone">
            <input
              type="file"
              accept="video/*"
              onChange={(event) => {
                setFile(event.target.files[0] || null);
                setError("");
                setResult(null);
              }}
            />
            <div className="upload-icon">↑</div>
            <strong>
              {file ? file.name : "Choose a video to upload"}
            </strong>
            <span>
              {file
                ? `${(file.size / (1024 * 1024)).toFixed(2)} MB`
                : "Click here to browse your files"}
            </span>
          </label>

          <button
            className="analyze-button"
            onClick={analyzeVideo}
            disabled={!file || loading}
          >
            {loading ? "Analyzing video..." : "Analyze video →"}
          </button>

          {loading && (
            <p className="loading-note">
              This may take a few minutes while the video is transcribed
              and analyzed.
            </p>
          )}

          {error && <div className="error-message">{error}</div>}
        </section>

        {result && (
          <section className="results">
            <div className="section-heading">
              <div>
                <span className="eyebrow">ANALYSIS COMPLETE</span>
                <h2>Video analysis</h2>
              </div>
              <span className="file-label">{file?.name}</span>
            </div>

            {report && (
              <div className="stats-grid">
                <div className="stat-card score-card">
                  <span>Claim-support score</span>
                  <strong>
                    {report.trust_score == null
                      ? "N/A"
                      : `${report.trust_score}%`}
                  </strong>
                  <small>Among decisive verdicts</small>
                </div>
                <div className="stat-card">
                  <span>Coverage</span>
                  <strong>{report.coverage}%</strong>
                  <small>Claims with decisive verdicts</small>
                </div>
                <div className="stat-card">
                  <span>Claims analyzed</span>
                  <strong>{report.total_claims}</strong>
                  <small>Total extracted claims</small>
                </div>
                <div className="stat-card">
                  <span>Supported</span>
                  <strong>{report.supported}</strong>
                  <small>
                    {report.contradicted} contradicted ·{" "}
                    {report.insufficient} insufficient
                  </small>
                </div>
              </div>
            )}

            <div className="content-card">
              <h3>Transcript</h3>
              <p className="transcript">{result.transcript}</p>
            </div>

            <div className="section-heading claims-heading">
              <div>
                <span className="eyebrow">CLAIM-BY-CLAIM REVIEW</span>
                <h2>Extracted claims</h2>
              </div>
            </div>

            {(result.verification || []).map((item, index) => {
              const verdict = item.verification?.verdict;
              const evidenceGroup = (result.evidence || []).find(
                (entry) => entry.claim === item.claim
              );

              const evidence = [
                ...(evidenceGroup?.local_evidence || []),
                ...(evidenceGroup?.web_evidence || []),
              ];

              return (
                <article className="claim-card" key={index}>
                  <div className="claim-top">
                    <span className="claim-number">
                      CLAIM {String(index + 1).padStart(2, "0")}
                    </span>
                    <span className={`verdict ${verdictClass(verdict)}`}>
                      {verdict || "INSUFFICIENT"}
                    </span>
                  </div>

                  <h3>{item.claim}</h3>
                  <p className="reason">
                    {item.verification?.reason}
                  </p>

                  <details>
                    <summary>
                      View evidence ({evidence.length})
                    </summary>
                    <div className="evidence-list">
                      {evidence.length === 0 ? (
                        <p>No evidence was retrieved.</p>
                      ) : (
                        evidence.map((entry, evidenceIndex) => (
                          <div
                            className="evidence-item"
                            key={evidenceIndex}
                          >
                            <span className="evidence-source">
                              {entry.source === "web"
                                ? "WEB"
                                : "LOCAL RAG"}
                            </span>
                            <strong>
                              {entry.title || entry.source || "Evidence"}
                            </strong>
                            <p>{entry.text}</p>
                            {entry.url && (
                              <a
                                href={entry.url}
                                target="_blank"
                                rel="noreferrer"
                              >
                                Open source ↗
                              </a>
                            )}
                          </div>
                        ))
                      )}
                    </div>
                  </details>
                </article>
              );
            })}
          </section>
        )}

        <footer>
          VeriVid · AI-assisted fact-checking · Evidence-based analysis
        </footer>
      </main>
    </div>
  );
}

export default App;