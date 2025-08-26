// Mock users for development/testing
export const DEFAULT_USERS = [
  {
    staffId: 'admin',
    password: 'admin123',
    user: {
      id: 1,
      staffId: 'admin',
      fullName: 'Nguyễn Văn Admin',
      department: 'Phòng Pháp chế',
      role: 'Administrator',
      permissions: ['chat', 'documents', 'admin']
    }
  },
  {
    staffId: 'legal01',
    password: 'legal123',
    user: {
      id: 2,
      staffId: 'legal01',
      fullName: 'Trần Thị Pháp',
      department: 'Phòng Pháp chế',
      role: 'Legal Officer',
      permissions: ['chat', 'documents']
    }
  },
  {
    staffId: 'credit01',
    password: 'credit123',
    user: {
      id: 3,
      staffId: 'credit01',
      fullName: 'Lê Văn Tín',
      department: 'Phòng Tín dụng',
      role: 'Credit Officer',
      permissions: ['chat']
    }
  },
  {
    staffId: 'demo',
    password: 'demo',
    user: {
      id: 4,
      staffId: 'demo',
      fullName: 'Người dùng Demo',
      department: 'Demo Department',
      role: 'Demo User',
      permissions: ['chat', 'documents']
    }
  }
];

// Mock authentication function
export const mockLogin = (staffId, password) => {
  return new Promise((resolve, reject) => {
    // Simulate API delay
    setTimeout(() => {
      const user = DEFAULT_USERS.find(u => u.staffId === staffId && u.password === password);
      
      if (user) {
        resolve({
          token: `mock-jwt-token-${Date.now()}`,
          user: user.user,
          message: 'Đăng nhập thành công'
        });
      } else {
        reject({
          response: {
            data: {
              message: 'Mã nhân viên hoặc mật khẩu không đúng'
            }
          }
        });
      }
    }, 800); // Simulate network delay
  });
};
