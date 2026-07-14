import { useEffect, useState } from "react";
import api from "../lib/api.js";

export default function Library() {
  const [projects, setProjects] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get("/projects")
      .then(({ data }) => setProjects(data))
      .catch((e) => setError(e?.response?.data?.detail || "Failed to load projects."))
      .finally(() => setLoading(false));
  }, []);

  async function handleDelete(id) {
    await api.delete(`/projects/${id}`);
    setProjects((prev) => prev.filter((p) => p.id !== id));
  }

  return (
    <div className="p-8 space-y-4">
      <h1 className="text-2xl font-semibold">Library</h1>

      {loading && <p className="text-muted text-sm">Loading…</p>}
      {error && <p className="text-red-400 text-sm">{error}</p>}

      {!loading && !error && projects.length === 0 && (
        <div className="glass rounded-xl2 p-5 text-muted text-sm">
          No projects yet — create one from Create Video.
        </div>
      )}

      <div className="grid gap-3">
        {projects.map((p) => (
          <div key={p.id} className="glass rounded-xl2 p-4 flex items-center justify-between">
            <div>
              <div className="font-medium">{p.topic}</div>
              <div className="text-xs text-muted mt-1">
                {p.target_length} · {p.status}
                {p.youtube_url && (
                  <>
                    {" · "}
                    <a href={p.youtube_url} target="_blank" rel="noreferrer" className="underline">
                      View on YouTube
                    </a>
                  </>
                )}
              </div>
            </div>
            <button
              onClick={() => handleDelete(p.id)}
              className="text-xs text-muted hover:text-red-400 border border-white/10 rounded-xl2 px-3 py-1.5"
            >
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
