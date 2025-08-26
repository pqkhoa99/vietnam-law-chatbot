import { useState } from 'react';

export const useChat = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const addMessage = (message, type = 'user') => {
    const newMessage = {
      id: Date.now(),
      message,
      type,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, newMessage]);
  };

  const clearMessages = () => {
    setMessages([]);
  };

  return {
    messages,
    isLoading,
    setIsLoading,
    addMessage,
    clearMessages,
    setMessages,
  };
};
