import { useMemo } from 'react'

const DEFAULT_AGENTS = [
  { id: 'preference_analyzer', name: 'Preference Analyzer', description: 'Extracting your travel preferences...', icon: '🔍' },
  { id: 'researcher', name: 'Research Agent', description: 'Discovering top attractions & activities...', icon: '🌍' },
  { id: 'itinerary_planner', name: 'Itinerary Planner', description: 'Crafting your day-by-day plan...', icon: '📋' },
  { id: 'final_responder', name: 'Final Responder', description: 'Compiling your personalized travel plan...', icon: '✨' },
]

function AgentPipeline({ agents, completedAgents }) {
  const agentList = agents.length > 0 ? agents : DEFAULT_AGENTS

  const activeIndex = useMemo(() => {
    if (completedAgents.length === agentList.length) return -1
    return completedAgents.length
  }, [completedAgents, agentList])

  return (
    <div className="pipeline-overlay" id="pipeline-overlay">
      <div className="pipeline-container">
        <div className="pipeline-card">
          <div className="pipeline-header">
            <h2>🧠 AI Agents at Work</h2>
            <p>Your travel plan is being crafted by our team of AI agents</p>
          </div>

          <div className="pipeline-steps">
            {agentList.map((agent, index) => {
              const isCompleted = completedAgents.includes(agent.id)
              const isActive = index === activeIndex
              const isPending = !isCompleted && !isActive

              let stepClass = 'pipeline-step'
              if (isCompleted) stepClass += ' completed'
              else if (isActive) stepClass += ' active'
              else stepClass += ' pending'

              return (
                <div key={agent.id} className={stepClass}>
                  <div className="pipeline-step-icon">
                    {isCompleted ? '✓' : agent.icon}
                  </div>
                  <div className="pipeline-step-content">
                    <div className="pipeline-step-name">{agent.name}</div>
                    <div className="pipeline-step-desc">{agent.description}</div>
                  </div>
                  <div className="pipeline-step-status">
                    {isCompleted && 'Done'}
                    {isActive && (
                      <div className="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                      </div>
                    )}
                    {isPending && 'Waiting'}
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </div>
    </div>
  )
}

export default AgentPipeline
