import { Shield, Zap, Lock, Search, Activity, AlertTriangle } from 'lucide-react';

const features = [
  {
    icon: Shield,
    title: 'Comprehensive Protection',
    description: 'Multi-layered security analysis detecting vulnerabilities across headers, SSL/TLS, and application stack.',
  },
  {
    icon: Zap,
    title: 'Lightning Fast Scans',
    description: 'Advanced scanning engine delivers results in seconds, not hours. Real-time analysis for immediate insights.',
  },
  {
    icon: Search,
    title: 'Deep Technology Detection',
    description: 'Identify frameworks, libraries, and technologies with precision using hybrid detection methods.',
  },
  {
    icon: Lock,
    title: 'SSL/TLS Analysis',
    description: 'Complete certificate validation, cipher suite analysis, and protocol security assessment.',
  },
  {
    icon: Activity,
    title: 'AI-Powered Insights',
    description: 'Machine learning algorithms provide intelligent risk assessment and actionable recommendations.',
  },
  {
    icon: AlertTriangle,
    title: 'Vulnerability Intelligence',
    description: 'Integration with NVD and OSV databases for real-time CVE and security advisory tracking.',
  },
];

export function Features() {
  return (
    <section className="py-32 bg-cream-light">
      <div className="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
        <div className="text-center space-y-4 mb-20">
          <h2 className="text-5xl sm:text-6xl font-bold text-brown">
            Enterprise-Grade Security Analysis
          </h2>
          <p className="text-lg text-brown/60 max-w-3xl mx-auto font-medium">
            Built for security professionals, powered by cutting-edge technology
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="group p-8 rounded-2xl bg-cream hover:shadow-lg transition-all duration-300 border border-brown/10 hover:border-coral/30"
            >
              <div className="w-12 h-12 rounded-xl bg-coral group-hover:bg-coral-dark flex items-center justify-center mb-6 transition-colors">
                <feature.icon className="w-6 h-6 text-cream" />
              </div>
              <h3 className="text-lg font-bold text-brown mb-3 transition-colors">
                {feature.title}
              </h3>
              <p className="text-brown/60 leading-relaxed transition-colors font-medium">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
