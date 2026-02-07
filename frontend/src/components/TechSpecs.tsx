import { Database, Cpu, Layers, Shield } from 'lucide-react';

const specs = [
  {
    category: 'Detection Methods',
    items: [
      { label: 'Regex Pattern Matching', value: 'Advanced' },
      { label: 'Header Analysis', value: 'Real-time' },
      { label: 'Wappalyzer Integration', value: '1000+ signatures' },
      { label: 'Hybrid Detection', value: 'Multi-source' },
    ],
  },
  {
    category: 'Vulnerability Sources',
    items: [
      { label: 'NVD Database', value: 'Integrated' },
      { label: 'OSV API', value: 'Real-time' },
      { label: 'CVE Tracking', value: 'Automatic' },
      { label: 'Security Advisories', value: 'Live updates' },
    ],
  },
  {
    category: 'AI Analysis',
    items: [
      { label: 'Risk Assessment', value: 'ML-powered' },
      { label: 'Recommendations', value: 'Contextual' },
      { label: 'Severity Scoring', value: 'Intelligent' },
      { label: 'Explanation Engine', value: 'Natural language' },
    ],
  },
  {
    category: 'Security Checks',
    items: [
      { label: 'SSL/TLS Validation', value: 'Complete' },
      { label: 'Certificate Analysis', value: 'Deep scan' },
      { label: 'Header Security', value: '15+ headers' },
      { label: 'Protocol Testing', value: 'TLS 1.0-1.3' },
    ],
  },
];

export function TechSpecs() {
  return (
    <section className="py-32 bg-brown">
      <div className="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
        <div className="text-center space-y-4 mb-20">
          <h2 className="text-5xl sm:text-6xl font-bold text-cream">
            Technical Specifications
          </h2>
          <p className="text-lg text-cream/70 max-w-3xl mx-auto font-medium">
            Built with industry-leading security standards and methodologies
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {specs.map((spec, index) => (
            <div
              key={index}
              className="p-8 rounded-2xl bg-brown-light/50 border border-coral/20"
            >
              <h3 className="text-2xl font-bold text-cream mb-6 flex items-center gap-3">
                {index === 0 && <Layers className="w-6 h-6 text-coral" />}
                {index === 1 && <Database className="w-6 h-6 text-coral" />}
                {index === 2 && <Cpu className="w-6 h-6 text-coral" />}
                {index === 3 && <Shield className="w-6 h-6 text-coral" />}
                {spec.category}
              </h3>
              <div className="space-y-4">
                {spec.items.map((item, idx) => (
                  <div key={idx} className="flex justify-between items-center py-3 border-b border-coral/10 last:border-0">
                    <span className="text-cream/80 font-medium">{item.label}</span>
                    <span className="text-coral font-semibold">{item.value}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="mt-12 p-8 rounded-2xl bg-coral">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div>
              <h3 className="text-2xl font-bold text-cream mb-2">
                Ready to secure your applications?
              </h3>
              <p className="text-cream/90 font-medium">
                Start scanning today with our comprehensive security platform
              </p>
            </div>
            <button className="px-8 py-4 bg-cream hover:bg-cream-light text-coral rounded-full font-semibold transition-all duration-200 whitespace-nowrap">
              Get Started
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
