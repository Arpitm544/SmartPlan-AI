import TripInput from './TripInput'

function HeroSection({ onSubmit, error }) {
  return (
    <section className="hero" id="hero-section">
      <div className="hero-glow" />
      <div className="hero-content">
        <div className="hero-tag">
          <span className="hero-tag-dot" />
          4 AI Agents Working Together
        </div>

        <h1 className="hero-title">
          Plan Your Dream Trip
          <br />
          with{' '}
          <span className="hero-title-gradient">AI Intelligence</span>
        </h1>

        <p className="hero-subtitle">
          Describe your perfect vacation and our multi-agent AI system will
          research destinations, craft itineraries, optimize your budget, and
          deliver a personalized travel plan in seconds.
        </p>

        <TripInput onSubmit={onSubmit} />

        {error && (
          <div className="error-banner" id="error-banner">
            {error}
          </div>
        )}
      </div>
    </section>
  )
}

export default HeroSection
