import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getAgents = async () => {
  try {
    const response = await api.get('/agents');
    return response.data;
  } catch (error) {
    console.error('Error fetching agents:', error);
    throw error;
  }
};

export const chatWithAgent = async (agentType, message) => {
  try {
    const response = await api.post('/chat', {
      agent_type: agentType,
      message: message,
      context: {}
    });
    return response.data;
  } catch (error) {
    console.error('Error chatting with agent:', error);
    throw error;
  }
};

export const healthCheck = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Error checking health:', error);
    throw error;
  }
};

export default api;