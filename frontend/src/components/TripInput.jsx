import { useState, useRef, useEffect } from 'react'

const SUGGESTIONS = [
  '🏯 India for 5 days, $2000, gaming & food',
  '🏖️ Plan a 2-day trip to Jaipur under 8000 rupess with historical places',
  '🏔️ Switzerland for 4 days, $3000, adventure & scenic',
  '🌆 New York for 3 days, $1800, sightseeing & Broadway',
]

function TripInput({ onSubmit }) {
  const [query, setQuery] = useState('')
  const textareaRef = useRef(null)

  // Auto-resize textarea
  useEffect(() => {
    const el = textareaRef.current
    if (el) {
      el.style.height = 'auto'
      el.style.height = Math.min(el.scrollHeight, 160) + 'px'
    }
  }, [query])

  const handleSubmit = () => {
    if (query.trim()) {
      onSubmit(query.trim())
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  const handleSuggestion = (text) => {
    // Remove the emoji prefix
    const cleaned = text.replace(/^[^\s]+\s/, '')
    setQuery(cleaned)
  }

  return (
    <div className="trip-input-wrapper" id="trip-input">
      <div className="trip-input-card">
        <div className="trip-input-inner">
          <textarea
            ref={textareaRef}
            className="trip-textarea"
            placeholder="Describe your dream trip... e.g., 'I want to explore Paris for 5 days with a $2500 budget, focusing on art, cafés, and history'"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            id="trip-query-input"
          />
          <button
            className="trip-submit-btn"
            onClick={handleSubmit}
            disabled={!query.trim()}
            id="trip-submit-btn"
            aria-label="Plan my trip"
          >
            →
          </button>
        </div>
      </div>

      <div className="trip-suggestions stagger-children">
        {SUGGESTIONS.map((s, i) => (
          <button
            key={i}
            className="trip-suggestion-chip animate-fade-in-up"
            onClick={() => handleSuggestion(s)}
            style={{ animationDelay: `${400 + i * 80}ms` }}
          >
            {s}
          </button>
        ))}
      </div>
    </div>
  )
}

export default TripInput
