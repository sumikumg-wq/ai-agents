import { useState } from "react";
import axios from "axios";

const LENGTHS = ["30s", "60s", "5min", "10min"];
const STAGES = [
  "Research", "Script", "Storyboard", "Voice", "Images",
  "Video", "Thumbnail", "SEO", "Upload",
];

export default function CreateVideo() {
  const [topic, setTopic] = useState("");
  const [length, setLength] = useState("60s");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  async function handleGenerate() {
    if (!topic.trim()) return;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const { data } = await axios.post("/api/agents/script", {
        topic,
        length,
      });
      setResult(data);
    } catch (e) {
      setError(e?.response?.data?.detail || "Generation failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="p-8 space-y-6 max-w-3xl">
      <h1 className="text-2xl font-semibold">Create Video</h1>

      <div className="glass rounded-xl2 p-5 space-y-4">
        <div>
          <label className="text-sm text-muted">Topic</label>
          <input
            className="w-full mt-1 bg-bg border border-white/10 rounded-xl2 px-3 py-2"
            placeholder="e.g. The Lost City of Atlantis"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
          />
        </div>

        <div>
          <label className="text-sm text-muted">Video Length</label>
          <div className="flex gap-2 mt-1">
            {LENGTHS.map((l) => (
              <button
                key={l}
                onClick={() => setLength(l)}
                className={`px-3 py-1.5 rounded-xl2 text-sm border ${
                  length === l
                    ? "bg-primary border-primary"
                    : "border-white/10 text-muted"
                }`}
              >
                {l}
              </button>
            ))}
          </div>
        </div>

        <button
          onClick={handleGenerate}
          disabled={loading}
          className="w-full bg-gradient-to-r from-primary to-accent rounded-xl2 py-2.5 font-medium disabled:opacity-50"
        >
          {loading ? "Generating…" : "Generate"}
        </button>

        {error && <p className="text-red-400 text-sm">{error}</p>}
      </div>

      <div className="glass rounded-xl2 p-5">
        <div className="text-sm text-muted mb-3">Generation Progress</div>
        <div className="flex flex-wrap gap-2">
          {STAGES.map((s) => (
            <span
              key={s}
              className={`text-xs px-2.5 py-1 rounded-full border ${
                s === "Script" && result
                  ? "border-primary text-text"
                  : "border-white/10 text-muted"
              }`}
            >
              {s}
            </span>
          ))}
        </div>
      </div>

      {result && (
        <div className="glass rounded-xl2 p-5 space-y-2">
          <div className="text-sm text-muted">
            Script ({result.estimated_word_count} words)
          </div>
          <p className="whitespace-pre-wrap text-sm leading-relaxed">
            {result.script}
          </p>
        </div>
      )}
    </div>
  );
}
