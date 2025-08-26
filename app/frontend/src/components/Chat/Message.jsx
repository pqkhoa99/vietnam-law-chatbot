import React, { useState, useEffect, useRef } from 'react';
import { marked } from 'marked';

const Message = ({ message, type, timestamp, relatedDocuments }) => {
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

  // Helper function to get relationship type title
  const getRelationshipTitle = (relaType, isIncoming = false) => {
    const titles = {
      'SUA_DOI_BO_SUNG': 'sửa đổi bổ sung',
      'HUONG_DAN_QUY_DINH': 'hướng dẫn quy định',
      'THAY_THE': 'thay thế',
      'BAI_BO': 'bãi bỏ',
      'DINH_CHI': 'đình chỉ'
    };
    
    const baseTitle = titles[relaType] || 'liên quan';
    return isIncoming ? `Bị ${baseTitle} bởi` : baseTitle.charAt(0).toUpperCase() + baseTitle.slice(1);
  };

  // Helper function to group relationships by type
  const groupRelationshipsByType = (relationships) => {
    return relationships.reduce((acc, rel) => {
      if (!acc[rel.rela_type]) {
        acc[rel.rela_type] = [];
      }
      acc[rel.rela_type].push(rel);
      return acc;
    }, {});
  };

  // Component for expandable content
  const ExpandableContent = ({ content, maxLength = 150 }) => {
    const [isExpanded, setIsExpanded] = useState(false);
    
    if (!content || content.length <= maxLength) {
      return <span>{content || 'N/A'}</span>;
    }

    return (
      <span>
        {isExpanded ? content : `${content.substring(0, maxLength)}...`}
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          style={{
            background: 'none',
            border: 'none',
            color: 'var(--accent-2)',
            cursor: 'pointer',
            textDecoration: 'underline',
            fontSize: 'inherit',
            padding: 0,
            marginLeft: '5px'
          }}
        >
          {isExpanded ? 'Thu gọn' : 'Xem thêm'}
        </button>
      </span>
    );
  };

  // Component for modal with markdown content
// Dialog component for displaying full document content
const DialogContent = ({ content, documentId }) => {
  const [isOpen, setIsOpen] = useState(false);
  const dialogRef = useRef(null);

  const openDialog = () => {
    setIsOpen(true);
    // Use setTimeout to ensure the dialog is in the DOM before calling showModal
    setTimeout(() => {
      if (dialogRef.current) {
        dialogRef.current.showModal();
      }
    }, 0);
  };

  const closeDialog = () => {
    if (dialogRef.current) {
      dialogRef.current.close();
    }
    setIsOpen(false);
  };

  // Handle dialog close event
  useEffect(() => {
    const dialog = dialogRef.current;
    if (dialog) {
      const handleClose = () => setIsOpen(false);
      dialog.addEventListener('close', handleClose);
      return () => dialog.removeEventListener('close', handleClose);
    }
  }, []);

  return (
    <>
      <span 
        className="document-title-link" 
        onClick={openDialog}
      >
        {content.split('\n')[0] || `Document ${documentId}`}
      </span>
      
      {isOpen && (
        <dialog 
          ref={dialogRef}
          className="document-dialog"
        >
          <div className="dialog-header">
            <h3>Document {documentId}</h3>
            <button
              onClick={closeDialog}
              className="dialog-close"
            >
              ×
            </button>
          </div>
          
          <div 
            className="dialog-body"
            dangerouslySetInnerHTML={{ 
              __html: marked.parse(content || 'No content available') 
            }} 
          />
        </dialog>
      )}
    </>
  );
};  // Render related documents as React elements
  const renderRelatedDocuments = () => {
    if (!relatedDocuments || relatedDocuments.length === 0) {
      return null;
    }

    return (
      <div className="related-documents">
        <hr />
        <h3>📚 Tài liệu liên quan</h3>
        {relatedDocuments.map((doc, index) => {
          let cutContent = doc.content;
          
          // Add formatting before each "Điều" for better readability, keeping all content
          if (cutContent) {
            // Add \n\n\t before each occurrence of "Điều" (except the first one if it's at the beginning)
            cutContent = cutContent.replace(/(\S.*?)(\s*Điều)/g, '$1\n\n\t$2');
          }
          
          return (
          <div key={index} className="document-item">
            <h3>
              <strong>{index + 1}. {doc.document_title} - {doc.title}</strong>
            </h3>
            <p>
              <em>Điểm tương đồng: {(doc.score * 100).toFixed(1)}%</em>
            </p>
            
            {/* Document metadata */}
            <div className="document-metadata">
              <span className={`status-badge ${doc.document_status === 'Còn hiệu lực' ? 'valid' : doc.document_status === 'Hết hiệu lực một phần' ? 'warning' : 'expired'}`}>
                {doc.document_status}
              </span>
              {doc.effective_date && (
                <span className="metadata-item">
                  <strong>Ngày hiệu lực:</strong> {doc.effective_date}
                </span>
              )}
              {doc.expired_date && (
                <span className="metadata-item">
                  <strong>Ngày hết hạn:</strong> {doc.expired_date}
                </span>
              )}
            </div>

            {/* Document content as markdown */}
            {cutContent && (
              <div className="document-content">
                <div dangerouslySetInnerHTML={{ __html: marked(cutContent.trim()) }} />
              </div>
            )}
            
            {/* Show relationships if they exist */}
            {doc.relationships && (doc.relationships.incoming.length > 0 || doc.relationships.outgoing.length > 0) && (
              <div className="relationships">
                <strong>Mối quan hệ pháp lý:</strong>
                
                {/* Incoming relationships */}
                {doc.relationships.incoming.length > 0 && (
                  <div className="relationship-section">
                    {Object.entries(groupRelationshipsByType(doc.relationships.incoming)).map(([relaType, rels]) => (
                      <div key={relaType} className="relationship-group">
                        <div className="relationship-title">
                          - <strong>{getRelationshipTitle(relaType, true)}:</strong>
                        </div>
                        <ul>
                          {rels.map((rel, relIndex) => (
                            <li key={relIndex}>
                              <a href={`#${rel.document_id}`}>[{rel.document_id}]</a>: <DialogContent content={rel.content} documentId={rel.document_id} />
                            </li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                )}
                
                {/* Outgoing relationships */}
                {doc.relationships.outgoing.length > 0 && (
                  <div className="relationship-section">
                    {Object.entries(groupRelationshipsByType(doc.relationships.outgoing)).map(([relaType, rels]) => (
                      <div key={relaType} className="relationship-group">
                        <div className="relationship-title">
                          - <strong>{getRelationshipTitle(relaType, false)}:</strong>
                        </div>
                        <ul>
                          {rels.map((rel, relIndex) => (
                            <li key={relIndex}>
                              <a href={`#${rel.document_id}`}>[{rel.document_id}]</a>: <DialogContent content={rel.content} documentId={rel.document_id} />
                            </li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        )})}
      </div>
    );
  };

  return (
    <div className={`msg ${type}`} role="article" aria-label={`Tin nhắn từ ${type === 'bot' ? 'trợ lý' : 'người dùng'}`}>
      <div dangerouslySetInnerHTML={renderContent()} />
      {renderRelatedDocuments()}
      {timestamp && (
        <div className="meta-line">
          <small>{new Date(timestamp).toLocaleTimeString('vi-VN')}</small>
        </div>
      )}
    </div>
  );
};

export default Message;
