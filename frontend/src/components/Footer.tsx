import { Shield, Github, Linkedin, Twitter } from 'lucide-react';

export function Footer() {
  return (
    <footer className="bg-brown border-t border-brown-light">
      <div className="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12 py-16">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-coral flex items-center justify-center">
                <Shield className="w-6 h-6 text-cream" />
              </div>
              <span className="text-xl font-bold text-cream">SecureScan</span>
            </div>
            <p className="text-cream/60 text-sm leading-relaxed font-medium">
              Building a world where web applications operate securely everywhere.
            </p>
          </div>

          <div>
            <h3 className="text-cream font-bold mb-4">Product</h3>
            <ul className="space-y-3">
              <li><a href="#" className="text-cream/60 hover:text-coral transition-colors font-medium">Features</a></li>
              <li><a href="#" className="text-cream/60 hover:text-coral transition-colors font-medium">Technical Specs</a></li>
              <li><a href="#" className="text-cream/60 hover:text-coral transition-colors font-medium">Pricing</a></li>
              <li><a href="#" className="text-cream/60 hover:text-coral transition-colors font-medium">Changelog</a></li>
            </ul>
          </div>

          <div>
            <h3 className="text-cream font-bold mb-4">Company</h3>
            <ul className="space-y-3">
              <li><a href="#" className="text-cream/60 hover:text-coral transition-colors font-medium">About</a></li>
              <li><a href="#" className="text-cream/60 hover:text-coral transition-colors font-medium">Careers</a></li>
              <li><a href="#" className="text-cream/60 hover:text-coral transition-colors font-medium">Blog</a></li>
              <li><a href="#" className="text-cream/60 hover:text-coral transition-colors font-medium">Contact</a></li>
            </ul>
          </div>

          <div>
            <h3 className="text-cream font-bold mb-4">Resources</h3>
            <ul className="space-y-3">
              <li><a href="#" className="text-cream/60 hover:text-coral transition-colors font-medium">Documentation</a></li>
              <li><a href="#" className="text-cream/60 hover:text-coral transition-colors font-medium">API Reference</a></li>
              <li><a href="#" className="text-cream/60 hover:text-coral transition-colors font-medium">Support</a></li>
              <li><a href="#" className="text-cream/60 hover:text-coral transition-colors font-medium">Status</a></li>
            </ul>
          </div>
        </div>

        <div className="pt-8 border-t border-brown-light flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-cream/60 text-sm font-medium">
            © 2026 SecureScan. All rights reserved.
          </p>
          <div className="flex items-center gap-6">
            <a href="#" className="text-cream/60 hover:text-coral transition-colors">
              <Github className="w-5 h-5" />
            </a>
            <a href="#" className="text-cream/60 hover:text-coral transition-colors">
              <Twitter className="w-5 h-5" />
            </a>
            <a href="#" className="text-cream/60 hover:text-coral transition-colors">
              <Linkedin className="w-5 h-5" />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
