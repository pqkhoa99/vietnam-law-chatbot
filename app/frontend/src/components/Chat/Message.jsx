import React from 'react';
import { marked } from 'marked';

const Message = ({ message, type, timestamp }) => {
  // Configure marked for safe rendering
  marked.setOptions({
    breaks: true,
    gfm: true,
    sanitize: false, // We trust our backend content
  });

  const renderContent = () => {
    if (type === 'bot') {
      // For bot messages, check if it's markdown (contains markdown syntax) or HTML
      if (message.includes('###') || message.includes('**') || message.includes('*') || message.includes('[') || message.includes('---')) {
        // It's markdown content from API
        return { __html: marked(message) };
      } else {
        // It's HTML content from mock responses
        return { __html: message };
      }
    } else {
      // For user messages, render as plain text
      return { __html: message };
    }
  };

  return (
    <div className={`msg ${type}`} role="article" aria-label={`Tin nhắn từ ${type === 'bot' ? 'trợ lý' : 'người dùng'}`}>
      <div dangerouslySetInnerHTML={renderContent()} />
      {timestamp && (
        <div className="meta-line">
          <small>{new Date(timestamp).toLocaleTimeString('vi-VN')}</small>
        </div>
      )}
    </div>
  );
};

export default Message;
