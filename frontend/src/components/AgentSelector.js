import React from 'react';
import './AgentSelector.css';

function AgentSelector({ agents, selectedAgent, onSelectAgent }) {
  return (
    <div className="agent-selector">
      <h2>选择Agent</h2>
      <div className="agent-buttons">
        {agents.map((agent) => (
          <button
            key={agent.type}
            className={`agent-button ${selectedAgent?.type === agent.type ? 'active' : ''}`}
            onClick={() => onSelectAgent(agent)}
          >
            {agent.name}
          </button>
        ))}
      </div>
      
      {selectedAgent && (
        <div className="agent-info">
          <h3>{selectedAgent.name}</h3>
          <p>{selectedAgent.description}</p>
          <div className="agent-status">
            状态: <span className={selectedAgent.status}>{selectedAgent.status}</span>
          </div>
        </div>
      )}
    </div>
  );
}

export default AgentSelector;