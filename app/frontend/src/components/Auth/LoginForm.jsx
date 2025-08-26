import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { DEFAULT_USERS } from '../../services/mockAuth';

const LoginForm = () => {
  const [formData, setFormData] = useState({
    staffId: '',
    password: '',
  });
  const [showCredentials, setShowCredentials] = useState(false);
  const { login, isLoading, error } = useAuth();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await login(formData.staffId, formData.password);
  };

  const handleQuickLogin = (staffId, password) => {
    setFormData({ staffId, password });
  };

  return (
    <div className="login-container">
      <div className="login-logo">URA</div>
      <h2 className="login-title">Đăng nhập URA-xLaw</h2>
      <p className="login-subtitle">
        Truy cập hệ thống AI pháp lý cho nhân viên ngân hàng
      </p>

      <form className="login-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="staff-id">Mã nhân viên</label>
          <input
            type="text"
            id="staff-id"
            name="staffId"
            placeholder="Nhập mã nhân viên"
            value={formData.staffId}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Mật khẩu</label>
          <input
            type="password"
            id="password"
            name="password"
            placeholder="Nhập mật khẩu"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        
        {error && (
          <div style={{ color: 'var(--danger)', fontSize: '14px', textAlign: 'center' }}>
            {error}
          </div>
        )}
        
        <button type="submit" className="login-btn" disabled={isLoading}>
          {isLoading ? (
            <>
              <i className="fas fa-spinner spinner"></i> Đang đăng nhập...
            </>
          ) : (
            'Đăng nhập'
          )}
        </button>
      </form>

      {/* Demo Credentials Section */}
      <div style={{ marginTop: '24px', padding: '16px', background: 'var(--glass)', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
          <span style={{ fontSize: '13px', fontWeight: '600', color: 'var(--muted)' }}>
            <i className="fas fa-info-circle"></i> Tài khoản Demo
          </span>
          <button
            type="button"
            onClick={() => setShowCredentials(!showCredentials)}
            style={{
              background: 'transparent',
              border: 'none',
              color: 'var(--accent)',
              cursor: 'pointer',
              fontSize: '12px',
              fontWeight: '600'
            }}
          >
            {showCredentials ? 'Ẩn' : 'Hiển thị'}
          </button>
        </div>
        
        {showCredentials && (
          <div style={{ fontSize: '12px', color: 'var(--muted)' }}>
            {DEFAULT_USERS.map((user, index) => (
              <div
                key={index}
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '8px',
                  margin: '4px 0',
                  background: 'var(--bg-900)',
                  borderRadius: '8px',
                  border: '1px solid var(--border-color)'
                }}
              >
                <div>
                  <div style={{ fontWeight: '600', color: 'var(--text)' }}>{user.user.fullName}</div>
                  <div>{user.staffId} / {user.password}</div>
                  <div style={{ fontSize: '11px', color: 'var(--muted)' }}>{user.user.department}</div>
                </div>
                <button
                  type="button"
                  onClick={() => handleQuickLogin(user.staffId, user.password)}
                  style={{
                    padding: '4px 8px',
                    background: 'var(--accent)',
                    color: '#fff',
                    border: 'none',
                    borderRadius: '6px',
                    fontSize: '11px',
                    cursor: 'pointer',
                    fontWeight: '600'
                  }}
                >
                  Sử dụng
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default LoginForm;
