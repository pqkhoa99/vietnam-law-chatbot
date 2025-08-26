import React from 'react';

const Message = ({ message, type, timestamp }) => {
  return (
    <div className={`msg ${type}`} role="article" aria-label={`Tin nhắn từ ${type === 'bot' ? 'trợ lý' : 'người dùng'}`}>
      <div dangerouslySetInnerHTML={{ __html: message }} />
      {timestamp && (
        <div className="meta-line">
          <small>{new Date(timestamp).toLocaleTimeString('vi-VN')}</small>
        </div>
      )}
    </div>
  );
};

export default Message;
