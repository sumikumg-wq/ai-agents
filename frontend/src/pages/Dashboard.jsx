const stats = [
  { label: "Total Videos", value: "0" },
  { label: "Views", value: "0" },
  { label: "Subscribers", value: "0" },
  { label: "Est. Revenue", value: "$0" },
];

export default function Dashboard() {
  return (
    <div className="p-8 space-y-6">
      <h1 className="text-2xl font-semibold">Dashboard</h1>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {stats.map((s) => (
          <div key={s.label} className="glass rounded-xl2 p-5">
            <div className="text-muted text-sm">{s.label}</div>
            <div className="text-2xl font-semibold mt-1">{s.value}</div>
          </div>
        ))}
      </div>
      <div className="glass rounded-xl2 p-5">
        <div className="text-muted text-sm mb-2">Recent Videos</div>
        <div className="text-sm text-muted">
          No videos yet — generate your first one from Create Video.
        </div>
      </div>
    </div>
  );
}
