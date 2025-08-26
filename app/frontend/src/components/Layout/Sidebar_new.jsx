import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';

const Sidebar = () => {
  const { logout, user } = useAuth();
  const [theme, setTheme] = useState('dark');

  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
  };

  return (
    <aside className="sidebar" aria-label="Thanh điều hướng chính">
      <div>
        <div className="brand" role="banner">
          <div className="logo">URA</div>
          <div>
            <h1 style={{ fontSize: '14px', marginBottom: '4px' }}>URA-xLaw</h1>
            <p style={{ margin: '0' }}>AI pháp lý cho Ngân hàng</p>
            {user && (
              <p style={{ margin: '2px 0 0 0', fontSize: '11px', color: 'var(--accent)' }}>
                {user.fullName} • {user.department}
              </p>
            )}
          </div>
        </div>

        <nav className="nav" aria-label="Điều hướng chính">
          <a href="#" className="active">
            <i className="fas fa-comments"></i> <span>Chat</span>
          </a>
          <a href="#">
            <i className="fas fa-file-alt"></i> <span>Văn bản</span>
          </a>
          <a href="#">
            <i className="fas fa-tasks"></i> <span>Checklist</span>
          </a>
          <a href="#">
            <i className="fas fa-history"></i> <span>Lịch sử</span>
          </a>
        </nav>

        <div className="search-docs" style={{ marginTop: '16px' }}>
          <input placeholder="Tìm văn bản, điều, khoản..." aria-label="Tìm kiếm văn bản" />
          <button>
            <i className="fas fa-search"></i>
          </button>
        </div>

        <div className="recent" aria-label="Truy vấn gần đây" style={{ marginTop: '14px' }}>
          <div style={{ fontWeight: '700', color: 'var(--muted)' }}>Gần đây</div>
          <div className="item">
            <div>Checklist mở thẻ tín dụng</div>
            <small>14:02 • hôm nay</small>
          </div>
          <div className="item">
            <div>So sánh NĐ 10 và 99</div>
            <small>11:51 • hôm nay</small>
          </div>
          <div className="item">
            <div>Điều kiện vay thế chấp</div>
            <small>09:33 • 2 Thg 8</small>
          </div>
        </div>
      </div>

      <div className="sidebar-footer">
        <button
          className="footer-btn"
          onClick={toggleTheme}
          title="Chuyển đổi giao diện"
        >
          <i className={`fas fa-${theme === 'dark' ? 'sun' : 'moon'}`}></i>
          <span className="footer-btn-text">
            {theme === 'dark' ? 'Chế độ sáng' : 'Chế độ tối'}
          </span>
        </button>
        <button className="footer-btn" onClick={logout} title="Đăng xuất">
          <i className="fas fa-sign-out-alt"></i>
          <span className="footer-btn-text">Đăng xuất</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
