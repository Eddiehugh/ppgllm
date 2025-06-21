import React, { useState, useEffect } from 'react';
import './App.css';
import AgentSelector from './components/AgentSelector';
import ChatInterface from './components/ChatInterface';
import { getAgents, healthCheck } from './services/api';

function App() {
  const [agents, setAgents] = useState([]);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [systemStatus, setSystemStatus] = useState('checking');

  useEffect(() => {
    const initializeApp = async () => {
      try {
        // 检查系统健康状态
        const healthStatus = await healthCheck();
        setSystemStatus(healthStatus.status);
        
        // 获取可用的Agent列表
        const agentsData = await getAgents();
        setAgents(agentsData.agents || []);
        setIsLoading(false);
      } catch (err) {
        console.error('初始化失败:', err);
        setError('无法连接到服务器，请检查后端服务是否运行。');
        setIsLoading(false);
        setSystemStatus('unhealthy');
      }
    };

    initializeApp();
  }, []);

  const handleAgentSelect = (agent) => {
    setSelectedAgent(agent);
  };

  if (isLoading) {
    return (
      <div className="app-loading">
        <div className="loading-spinner"></div>
        <p>正在加载系统...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app-error">
        <h2>出错了</h2>
        <p>{error}</p>
        <button onClick={() => window.location.reload()}>重试</button>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>隐私政策智能生成系统</h1>
        <div className={`system-status ${systemStatus}`}>
          系统状态: {systemStatus === 'healthy' ? '正常' : '异常'}
        </div>
      </header>
      
      <main className="app-main">
        <AgentSelector 
          agents={agents} 
          selectedAgent={selectedAgent} 
          onSelectAgent={handleAgentSelect} 
        />
        
        <ChatInterface selectedAgent={selectedAgent} />
      </main>
      
      <footer className="app-footer">
        <p>基于AutoGen框架的多Agent隐私政策生成、合规检测和可读性检测系统</p>
      </footer>
    </div>
  );
}

export default App;