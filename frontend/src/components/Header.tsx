import { Shield, Menu, X } from 'lucide-react';
import { useState } from 'react';

export function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-cream/80 backdrop-blur-md border-b border-cream">
      <div className="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
        <div className="flex items-center justify-between h-20">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-brown flex items-center justify-center">
              <Shield className="w-6 h-6 text-cream" />
            </div>
            <span className="text-xl font-bold text-brown">SecureScan</span>
          </div>

          <nav className="hidden md:flex items-center gap-8">
            <a href="#product" className="text-brown hover:text-coral transition-colors font-medium">
              Home
            </a>
            <a href="#features" className="text-brown hover:text-coral transition-colors font-medium">
              Features
            </a>
            <a href="#specs" className="text-brown hover:text-coral transition-colors font-medium">
              Specifications
            </a>
            <a href="#docs" className="text-brown hover:text-coral transition-colors font-medium">
              Docs
            </a>
            <button className="px-6 py-2.5 bg-coral hover:bg-coral-dark text-cream rounded-full font-semibold transition-all duration-200 transform hover:scale-105">
              Start Scanning
            </button>
          </nav>

          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden text-brown p-2"
          >
            {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {isMenuOpen && (
        <div className="md:hidden bg-cream border-t border-rust/20">
          <nav className="px-6 py-4 space-y-4">
            <a href="#product" className="block text-brown hover:text-coral transition-colors font-medium">
              Home
            </a>
            <a href="#features" className="block text-brown hover:text-coral transition-colors font-medium">
              Features
            </a>
            <a href="#specs" className="block text-brown hover:text-coral transition-colors font-medium">
              Specifications
            </a>
            <a href="#docs" className="block text-brown hover:text-coral transition-colors font-medium">
              Docs
            </a>
            <button className="w-full px-6 py-2.5 bg-coral hover:bg-coral-dark text-cream rounded-full font-semibold transition-all duration-200">
              Start Scanning
            </button>
          </nav>
        </div>
      )}
    </header>
  );
}
