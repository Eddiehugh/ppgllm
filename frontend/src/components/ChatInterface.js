import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { chatWithAgent } from '../services/api';
import './ChatInterface.css';

function ChatInterface({ selectedAgent }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // 当选择新的Agent时，清空聊天记录
  useEffect(() => {
    if (selectedAgent) {
      setMessages([
        {
          role: 'agent',
          content: `您好，我是${selectedAgent.name}。有什么可以帮助您的吗？`
        }
      ]);
    } else {
      setMessages([]);
    }
  }, [selectedAgent]);

  // 自动滚动到最新消息
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!selectedAgent || !input.trim()) return;
    
    const userMessage = input.trim();
    setInput('');
    
    // 添加用户消息到聊天记录
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    
    // 显示加载状态
    setIsLoading(true);
    
    try {
      // 发送请求到后端
      const response = await chatWithAgent(selectedAgent.type, userMessage);
      
      // 添加Agent回复到聊天记录
      if (response.success) {
        setMessages(prev => [...prev, { 
          role: 'agent', 
          content: response.response || '抱歉，我无法处理您的请求。'
        }]);
      } else {
        setMessages(prev => [...prev, { 
          role: 'error', 
          content: `错误: ${response.error || '处理请求时出现问题'}`
        }]);
      }
    } catch (error) {
      console.error('发送消息失败:', error);
      setMessages(prev => [...prev, { 
        role: 'error', 
        content: `网络错误: ${error.message || '无法连接到服务器'}`
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  if (!selectedAgent) {
    return (
      <div className="chat-interface empty-state">
        <p>请先选择一个Agent开始对话</p>
      </div>
    );
  }

  return (
    <div className="chat-interface">
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}-message`}>
            <ReactMarkdown>{msg.content}</ReactMarkdown>
          </div>
        ))}
        
        {isLoading && (
          <div className="message loading-message">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      <form className="chat-input-form" onSubmit={handleSendMessage}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="输入您的消息..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !input.trim()}>
          发送
        </button>
      </form>
    </div>
  );
}

export default ChatInterface;