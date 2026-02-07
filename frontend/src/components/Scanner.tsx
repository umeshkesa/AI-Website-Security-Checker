import { useState } from 'react';
import { Search, Loader2, ShieldAlert } from 'lucide-react';

export function Scanner() {
  const [url, setUrl] = useState('');
  const [isScanning, setIsScanning] = useState(false);

  const handleScan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url) return;

    setIsScanning(true);
    setTimeout(() => {
      setIsScanning(false);
    }, 2000);
  };

  return (
    <section className="py-32 bg-cream">
      <div className="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
        <div className="max-w-4xl mx-auto">
          <div className="text-center space-y-4 mb-12">
            <h2 className="text-5xl sm:text-6xl font-bold text-brown">
              Scan Your Website
            </h2>
            <p className="text-lg text-brown/60 font-medium">
              Enter any URL to receive a comprehensive security analysis in seconds
            </p>
          </div>

          <form onSubmit={handleScan} className="relative">
            <div className="flex flex-col sm:flex-row gap-3">
              <div className="flex-1 relative">
                <input
                  type="url"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="https://example.com"
                  className="w-full px-6 py-4 text-base rounded-full border-2 border-brown/20 focus:border-coral focus:outline-none transition-colors bg-cream-light text-brown placeholder-brown/40"
                  required
                />
              </div>
              <button
                type="submit"
                disabled={isScanning}
                className="px-10 py-4 bg-coral hover:bg-coral-dark disabled:bg-rust text-cream rounded-full font-semibold transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-70 whitespace-nowrap"
              >
                {isScanning ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Scanning...
                  </>
                ) : (
                  <>
                    <Search className="w-5 h-5" />
                    Scan Now
                  </>
                )}
              </button>
            </div>
          </form>

          <div className="mt-8 p-6 bg-cream-light rounded-2xl border border-brown/10">
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-lg bg-coral/10 flex items-center justify-center flex-shrink-0">
                <ShieldAlert className="w-5 h-5 text-coral" />
              </div>
              <div>
                <h3 className="font-bold text-brown mb-1">What we analyze</h3>
                <p className="text-brown/60 text-sm leading-relaxed font-medium">
                  Security headers • SSL/TLS configuration • Technology stack • Known vulnerabilities • CVE databases • Best practice compliance • AI risk assessment
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
