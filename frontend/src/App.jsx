import { Routes, Route } from "react-router-dom";
import Sidebar from "./layouts/Sidebar.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import CreateVideo from "./pages/CreateVideo.jsx";
import Library from "./pages/Library.jsx";
import Analytics from "./pages/Analytics.jsx";
import Uploads from "./pages/Uploads.jsx";
import Settings from "./pages/Settings.jsx";

export default function App() {
  return (
    <div className="flex min-h-screen bg-bg text-text">
      <Sidebar />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/create" element={<CreateVideo />} />
          <Route path="/library" element={<Library />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/uploads" element={<Uploads />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </main>
    </div>
  );
}
