import React from 'react';

const RightPanel = ({ onInsertShortcut }) => {
  const handleShortcut = (shortcutText) => {
    if (onInsertShortcut) {
      onInsertShortcut(shortcutText);
    }
  };

  return (
    <aside className="panel" aria-label="Tài liệu tham khảo">
      <h3>Tham chiếu nhanh</h3>
      <div className="doc-card">
        <div className="title">
          <i className="fas fa-file-alt"></i> Thông tư 39/2016/TT-NHNN
        </div>
        <div className="meta">Quy định về hoạt động cho vay</div>
      </div>
      <div className="doc-card">
        <div className="title">
          <i className="fas fa-file-alt"></i> Thông tư 19/2016/TT-NHNN
        </div>
        <div className="meta">Quy định về hoạt động thẻ ngân hàng</div>
      </div>

      <h3 style={{ marginTop: '16px' }}>Tác vụ Nâng cao</h3>
      <div className="shortcuts">
        <div
          className="chip"
          onClick={() => handleShortcut('Tạo checklist tuân thủ cho việc mở thẻ tín dụng')}
        >
          <i className="fas fa-tasks"></i> Tạo Checklist
        </div>
        <div
          className="chip"
          onClick={() => handleShortcut('So sánh Nghị định 10/2023 và 99/2022 về đăng ký tsđb')}
        >
          <i className="fas fa-exchange-alt"></i> So sánh Văn bản
        </div>
      </div>
    </aside>
  );
};

export default RightPanel;
