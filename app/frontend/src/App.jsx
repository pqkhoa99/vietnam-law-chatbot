import React from 'react';
import { AuthProvider } from './context/AuthContext';
import { useAuth } from './hooks/useAuth';
import LoginForm from './components/Auth/LoginForm';
import Sidebar from './components/Layout/Sidebar';
import RightPanel from './components/Layout/RightPanel';
import ChatInterface from './components/Chat/ChatInterface';
import './styles/globals.css';

const AppContent = () => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh' 
      }}>
        <i className="fas fa-spinner spinner" style={{ fontSize: '24px' }}></i>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <LoginForm />;
  }

  return (
    <div className="app" role="application" aria-label="URA-xLaw Chatbot">
      <Sidebar />
      <ChatInterface />
      <RightPanel />
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
