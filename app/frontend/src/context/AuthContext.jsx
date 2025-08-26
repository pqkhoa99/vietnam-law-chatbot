import React, { createContext, useReducer, useEffect } from 'react';
import { authAPI } from '../services/api';
import { mockLogin } from '../services/mockAuth';

export const AuthContext = createContext();

const authReducer = (state, action) => {
  switch (action.type) {
    case 'LOGIN_START':
      return {
        ...state,
        isLoading: true,
        error: null,
      };
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        isLoading: false,
        isAuthenticated: true,
        user: action.payload.user,
        token: action.payload.token,
        error: null,
      };
    case 'LOGIN_FAILURE':
      return {
        ...state,
        isLoading: false,
        isAuthenticated: false,
        user: null,
        token: null,
        error: action.payload,
      };
    case 'LOGOUT':
      return {
        ...state,
        isAuthenticated: false,
        user: null,
        token: null,
        error: null,
      };
    case 'SET_USER':
      return {
        ...state,
        user: action.payload,
        isAuthenticated: true,
      };
    default:
      return state;
  }
};

const initialState = {
  isAuthenticated: false,
  user: null,
  token: null,
  isLoading: false,
  error: null,
};

export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Check for existing token on app start
  useEffect(() => {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    
    if (token && user) {
      dispatch({
        type: 'LOGIN_SUCCESS',
        payload: {
          token,
          user: JSON.parse(user),
        },
      });
    }
  }, []);

  const login = async (staffId, password) => {
    dispatch({ type: 'LOGIN_START' });
    
    try {
      // Try real API first
      const response = await authAPI.login(staffId, password);
      
      // Store token and user info
      localStorage.setItem('token', response.token);
      localStorage.setItem('user', JSON.stringify(response.user));
      
      dispatch({
        type: 'LOGIN_SUCCESS',
        payload: {
          token: response.token,
          user: response.user,
        },
      });
      
      return { success: true };
    } catch (apiError) {
      console.log('Real API not available, trying mock authentication...', apiError.message);
      
      try {
        // Fallback to mock authentication
        const mockResponse = await mockLogin(staffId, password);
        
        // Store token and user info
        localStorage.setItem('token', mockResponse.token);
        localStorage.setItem('user', JSON.stringify(mockResponse.user));
        
        dispatch({
          type: 'LOGIN_SUCCESS',
          payload: {
            token: mockResponse.token,
            user: mockResponse.user,
          },
        });
        
        return { success: true };
      } catch (mockError) {
        const errorMessage = mockError.response?.data?.message || 'Đăng nhập thất bại';
        dispatch({
          type: 'LOGIN_FAILURE',
          payload: errorMessage,
        });
        return { success: false, error: errorMessage };
      }
    }
  };

  const logout = async () => {
    try {
      await authAPI.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Clear local storage
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      
      dispatch({ type: 'LOGOUT' });
    }
  };

  const value = {
    ...state,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
