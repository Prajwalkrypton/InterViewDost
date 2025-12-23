import { Button } from "./ui/button";

export function Header() {
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
          <a href="#technology" className="text-zinc-400 hover:text-white transition-colors">
            Technology
          </a>
          <a href="#about" className="text-zinc-400 hover:text-white transition-colors">
            About
          </a>
        </div>

        {/* CTA Buttons */}
        <div className="flex items-center gap-4">
          <Button variant="ghost" className="text-white hover:bg-zinc-900">
            Sign In
          </Button>
          <Button className="bg-white text-black hover:bg-zinc-200">
            Get Started
          </Button>
        </div>
      </nav>
    </header>
  );
}
