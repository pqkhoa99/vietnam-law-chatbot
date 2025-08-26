import axios from 'axios';

// Default to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API calls
export const authAPI = {
  login: async (staffId, password) => {
    const response = await api.post('/api/auth/login', {
      staff_id: staffId,
      password: password,
    });
    return response.data;
  },
  
  logout: async () => {
    const response = await api.post('/api/auth/logout');
    return response.data;
  },
  
  getCurrentUser: async () => {
    const response = await api.get('/api/auth/me');
    return response.data;
  },
};

// Chat API calls
export const chatAPI = {
  sendMessage: async (message) => {
    const response = await api.post('/api/v1/chat', {
      message: message,
    });
    return response.data;
  },
  
  getChatHistory: async () => {
    const response = await api.get('/api/chat/history');
    return response.data;
  },
  
  createNewChat: async () => {
    const response = await api.post('/api/chat/new');
    return response.data;
  },
};

// Document API calls (for future use)
export const documentAPI = {
  searchDocuments: async (query) => {
    const response = await api.get('/api/documents/search', {
      params: { q: query },
    });
    return response.data;
  },
  
  getDocument: async (documentId) => {
    const response = await api.get(`/api/documents/${documentId}`);
    return response.data;
  },
};

export default api;
