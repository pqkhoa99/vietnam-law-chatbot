import React, { useState } from 'react';

const MessageInput = ({ onSendMessage, isLoading }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="composer" role="region" aria-label="Khung soạn tin">
      <form onSubmit={handleSubmit} className="composer-main">
        <div className="composer-input">
          <input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Nhập câu hỏi của bạn (vd: quy định về TSĐB)..."
            aria-label="Đặt một câu hỏi"
            disabled={isLoading}
          />
          <div className="composer-tools">
            <button type="button" className="tool-btn" title="Đính kèm tệp">
              <i className="fas fa-paperclip"></i>
            </button>
          </div>
        </div>
      </form>
      <button
        type="button"
        className="send-btn"
        onClick={handleSubmit}
        disabled={isLoading || !message.trim()}
      >
        <i className="fas fa-paper-plane"></i>
      </button>
    </div>
  );
};

export default MessageInput;
