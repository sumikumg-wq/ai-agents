import { NavLink } from "react-router-dom";
import {
  LayoutDashboard, BarChart2, Library, UploadCloud, Settings, Sparkles,
} from "lucide-react";

const links = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard },
  { to: "/create", label: "Create Video", icon: Sparkles },
  { to: "/library", label: "Library", icon: Library },
  { to: "/analytics", label: "Analytics", icon: BarChart2 },
  { to: "/uploads", label: "Uploads", icon: UploadCloud },
  { to: "/settings", label: "Settings", icon: Settings },
];

export default function Sidebar() {
  return (
    <aside className="w-60 shrink-0 h-screen sticky top-0 border-r border-white/5 p-4 flex flex-col gap-1">
      <div className="text-lg font-semibold px-2 py-4 bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
        Chronicle AI
      </div>
      {links.map(({ to, label, icon: Icon }) => (
        <NavLink
          key={to}
          to={to}
          end={to === "/"}
          className={({ isActive }) =>
            `flex items-center gap-3 px-3 py-2 rounded-xl2 text-sm transition-colors ${
              isActive
                ? "bg-primary/20 text-text"
                : "text-muted hover:bg-card hover:text-text"
            }`
          }
        >
          <Icon size={18} />
          {label}
        </NavLink>
      ))}
    </aside>
  );
}
