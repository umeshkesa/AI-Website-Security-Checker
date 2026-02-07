import { Shield, Scan } from 'lucide-react';

export function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center bg-cream overflow-hidden pt-20">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(230,126,80,0.06),transparent_50%)]"></div>
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_70%_80%,rgba(139,111,71,0.04),transparent_50%)]"></div>

      <div className="relative max-w-7xl mx-auto px-6 sm:px-8 lg:px-12 py-32">
        <div className="text-center space-y-8">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-coral/10 border border-coral/30">
            <Shield className="w-4 h-4 text-coral" />
            <span className="text-sm font-semibold text-coral">Security-First Scanning</span>
          </div>

          <h1 className="text-6xl sm:text-7xl lg:text-8xl font-bold text-brown leading-tight tracking-tight">
            Scan, analyze,
            <br />
            <span className="text-coral">
              protect.
            </span>
          </h1>

          <p className="text-lg sm:text-xl text-brown/70 max-w-3xl mx-auto leading-relaxed font-medium">
            Comprehensive vulnerability detection powered by AI. Scan and protect your web applications with enterprise-grade security insights.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-8">
            <button className="group px-8 py-4 bg-coral hover:bg-coral-dark text-cream rounded-full font-semibold transition-all duration-200 flex items-center gap-2 transform hover:scale-105">
              <Scan className="w-5 h-5" />
              Start Free Scan
              <span className="group-hover:translate-x-1 transition-transform">→</span>
            </button>
            <button className="px-8 py-4 bg-transparent hover:bg-brown/5 text-brown rounded-full font-semibold transition-all duration-200 border-2 border-brown">
              View Documentation
            </button>
          </div>

          <div className="pt-12 flex flex-col sm:flex-row items-center justify-center gap-8 text-brown/60 text-sm font-medium">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-coral"></div>
              <span>Real-time Analysis</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-coral"></div>
              <span>AI-Powered</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-coral"></div>
              <span>Zero Configuration</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
