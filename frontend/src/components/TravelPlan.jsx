import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

const TABS = [
  { id: 'full', label: '📄 Full Plan' },
  { id: 'itinerary', label: '📋 Itinerary' },
  { id: 'budget', label: '💰 Budget' },
  { id: 'attractions', label: '🌍 Attractions' },
]

function TravelPlan({ data, onNewPlan }) {
  const [activeTab, setActiveTab] = useState('full')

  const getContent = () => {
    switch (activeTab) {
      case 'full':
        return data.final_plan || 'No plan available.'
      case 'itinerary':
        return data.itinerary || 'No itinerary data.'
      case 'budget':
        return data.budget_breakdown || 'No budget data.'
      case 'attractions':
        return data.attractions || 'No attractions data.'
      default:
        return data.final_plan
    }
  }

  return (
    <section className="plan-section" id="travel-plan">
      <div className="plan-header">
        <span className="plan-header-icon">🎉</span>
        <h1>Your Travel Plan is Ready!</h1>
        <div className="plan-header-meta">
          {data.destination && (
            <div className="plan-meta-item">
              <span className="plan-meta-icon">📍</span>
              {data.destination}
            </div>
          )}
          {data.num_days > 0 && (
            <div className="plan-meta-item">
              <span className="plan-meta-icon">📅</span>
              {data.num_days} {data.num_days === 1 ? 'Day' : 'Days'}
            </div>
          )}
          {data.budget && (
            <div className="plan-meta-item">
              <span className="plan-meta-icon">💵</span>
              {data.budget}
            </div>
          )}
          {data.preferences && data.preferences.length > 0 && (
            <div className="plan-meta-item">
              <span className="plan-meta-icon">❤️</span>
              {data.preferences.join(', ')}
            </div>
          )}
        </div>
      </div>

      <div className="plan-tabs" id="plan-tabs">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            className={`plan-tab ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
            id={`tab-${tab.id}`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="plan-content-card" id="plan-content">
        <div className="plan-markdown">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {getContent()}
          </ReactMarkdown>
        </div>
      </div>

      <div style={{ textAlign: 'center' }}>
        <button className="new-plan-btn" onClick={onNewPlan} id="new-plan-btn">
          ✨ Plan Another Trip
        </button>
      </div>
    </section>
  )
}

export default TravelPlan
