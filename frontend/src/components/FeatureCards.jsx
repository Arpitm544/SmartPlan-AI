const FEATURES = [
  {
    icon: '🔍',
    iconClass: '',
    title: 'Preference Analyzer',
    description:
      'Our AI instantly understands your travel style, budget constraints, and interests from a single natural language prompt.',
  },
  {
    icon: '🌍',
    iconClass: 'research',
    title: 'Smart Research Agent',
    description:
      'Discovers the most relevant attractions, hidden gems, and experiences that perfectly match your unique preferences.',
  },
  {
    icon: '📋',
    iconClass: 'itinerary',
    title: 'Itinerary Planner',
    description:
      'Crafts a balanced day-by-day travel plan, grouping locations logically so you can enjoy your trip without feeling rushed.',
  },
  {
    icon: '✨',
    iconClass: 'responder',
    title: 'Final Responder',
    description:
      'Synthesizes all the research, budget estimates, and itineraries into one polished, easy-to-read travel plan.',
  },
]

function FeatureCards() {
  return (
    <section className="features-section" id="features">
      <p className="features-label animate-fade-in-up">How it works</p>
      <h2 className="features-heading animate-fade-in-up">
        4 AI Agents, One Perfect Plan
      </h2>

      <div className="features-grid stagger-children">
        {FEATURES.map((f, i) => (
          <div
            key={i}
            className="glass-card feature-card animate-fade-in-up"
            style={{ animationDelay: `${i * 120}ms` }}
          >
            <div className={`feature-icon ${f.iconClass}`}>{f.icon}</div>
            <h3>{f.title}</h3>
            <p>{f.description}</p>
          </div>
        ))}
      </div>
    </section>
  )
}

export default FeatureCards
