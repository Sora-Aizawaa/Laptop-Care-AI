import { NavLink } from "react-router-dom";

const linkClass = ({ isActive }: { isActive: boolean }) =>
  `px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
    isActive ? "bg-brand-500 text-white" : "text-gray-600 hover:bg-gray-100"
  }`;

export default function Navbar() {
  return (
    <header className="sticky top-0 z-20 bg-white/90 backdrop-blur border-b border-gray-200">
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <NavLink to="/" className="flex items-center gap-2 font-bold text-lg text-brand-700">
          <span className="text-2xl">💻</span> LaptopCare AI
        </NavLink>
        <nav className="flex items-center gap-1">
          <NavLink to="/" end className={linkClass}>
            Home
          </NavLink>
          <NavLink to="/history" className={linkClass}>
            History
          </NavLink>
          <NavLink to="/knowledge-base" className={linkClass}>
            Knowledge Base
          </NavLink>
          <NavLink to="/dashboard" className={linkClass}>
            Technician Dashboard
          </NavLink>
        </nav>
      </div>
    </header>
  );
}
