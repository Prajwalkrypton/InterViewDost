import { Button } from "./ui/button";
import { useNavigate } from "react-router-dom";

export function Header() {
  const navigate = useNavigate();
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-black/80 backdrop-blur-xl border-b border-zinc-800">
      <nav className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-white rounded-lg" />
          <span className="text-white text-xl">InterViewDost</span>
        </div>

        {/* Navigation Links */}
        <div className="hidden md:flex items-center gap-8">
          <a href="#features" className="text-zinc-400 hover:text-white transition-colors">
            Features
          </a>
          <a href="#how-it-works" className="text-zinc-400 hover:text-white transition-colors">
            How It Works
          </a>
          <button
            type="button"
            className="text-zinc-400 hover:text-white transition-colors text-sm"
            onClick={() => navigate("/coding")}
          >
            Coding Prep
          </button>
          <button
            type="button"
            className="text-zinc-400 hover:text-white transition-colors text-sm"
            onClick={() => navigate("/community")}
          >
            Community
          </button>
        </div>

        {/* CTA Buttons */}
        <div className="flex items-center gap-4">
          <Button
            variant="ghost"
            className="text-white hover:bg-zinc-900"
            onClick={() => navigate("/login")}
          >
            Sign In
          </Button>
          <Button
            className="bg-white text-black hover:bg-zinc-200"
            onClick={() => navigate("/login")}
          >
            Get Started
          </Button>
        </div>
      </nav>
    </header>
  );
}
