# URA-xLaw Frontend

Vietnamese Legal Chatbot Frontend built with React + Vite for the Vietnam Law Chatbot project.

## 🎯 Overview

A complete React + Vite frontend for the Vietnamese Legal Chatbot (URA-xLaw) featuring a professional banking-style interface with authentication, real-time chat, and comprehensive legal assistant capabilities.

## ✨ Key Features

- 🔐 **Authentication**: Staff login with staff ID and password
- 💬 **Chat Interface**: Real-time chat with AI legal assistant
- 📱 **Responsive Design**: Works perfectly on desktop and mobile
- 🌓 **Dark/Light Theme**: Professional theme switching
- 🔗 **Backend Integration**: Seamless FastAPI backend connection
- 📝 **Legal Features**: Document comparison, checklist generation, citations
- 🇻🇳 **Vietnamese Localization**: Full Vietnamese language support
- 🎨 **Professional UI**: Banking-style interface with modern design

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. **Clone and navigate to the project**:
```bash
cd app/frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Configure environment**:
```bash
cp .env.example .env
```

4. **Update the `.env` file with your backend API URL**:
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_ENV=development
```

5. **Start the development server**:
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## 🔐 Authentication & Testing

### Default Login Credentials

For testing and development, the following demo accounts are available:

| **Staff ID** | **Password** | **Full Name** | **Department** | **Role** |
|--------------|--------------|---------------|----------------|----------|
| `admin` | `admin123` | Nguyễn Văn Admin | Phòng Pháp chế | Administrator |
| `legal01` | `legal123` | Trần Thị Pháp | Phòng Pháp chế | Legal Officer |
| `credit01` | `credit123` | Lê Văn Tín | Phòng Tín dụng | Credit Officer |
| `demo` | `demo123` | Người dùng Demo | Demo Department | Demo User |

### How to Test

1. **Open the app**: Navigate to `http://localhost:5173/`
2. **View credentials**: Click "Hiển thị" button on login page
3. **Quick login**: Click "Sử dụng" button next to any user
4. **Manual login**: Enter staff ID and password manually

**Note**: These are mock credentials for development only. When connected to a real backend, the app will use your actual authentication system.

### Features to Test

#### Authentication Flow
- ✅ Login with valid credentials
- ✅ Error message for invalid credentials  
- ✅ User info displayed in sidebar after login
- ✅ Logout functionality
- ✅ Session persistence (refresh page)

#### Chat Interface  
- ✅ Send messages
- ✅ Receive mock responses
- ✅ Mock legal responses for test queries:
  - "điều kiện cho vay thế chấp là gì?"
  - "tạo checklist mở thẻ tín dụng"
  - "so sánh nghị định 10/2023 và 99/2022 về đăng ký tsđb"

#### UI Features
- ✅ Dark/Light theme toggle
- ✅ Responsive design
- ✅ Vietnamese localization
- ✅ Professional banking interface

## 🔧 Technical Stack

- **Framework**: React 19.1.1
- **Build Tool**: Vite 7.1.3
- **HTTP Client**: Axios 1.11.0
- **Icons**: Font Awesome 7.0.0
- **Styling**: CSS Custom Properties (CSS Variables)
- **State Management**: React Context + Custom Hooks

## 📁 Project Structure

```
app/frontend/
├── src/
│   ├── components/
│   │   ├── Auth/
│   │   │   └── LoginForm.jsx          # Staff login form
│   │   ├── Chat/
│   │   │   ├── ChatInterface.jsx      # Main chat component
│   │   │   ├── Message.jsx            # Individual message bubble
│   │   │   └── MessageInput.jsx       # Message input with send button
│   │   ├── Layout/
│   │   │   ├── Sidebar.jsx           # Left navigation sidebar
│   │   │   └── RightPanel.jsx        # Right reference panel
│   │   └── Common/                   # Shared components
│   ├── context/
│   │   └── AuthContext.jsx           # Authentication state management
│   ├── hooks/
│   │   ├── useAuth.js               # Authentication hook
│   │   └── useChat.js               # Chat management hook
│   ├── services/
│   │   ├── api.js                   # Backend API integration
│   │   └── mockAuth.js              # Mock authentication service
│   ├── styles/
│   │   └── globals.css              # Complete UI styles
│   ├── App.jsx                      # Main app component
│   └── main.jsx                     # App entry point
├── public/                          # Static assets
├── .env                             # Environment configuration
├── .env.example                     # Environment template
├── build.sh                         # Build script
├── package.json                     # Dependencies and scripts
└── README.md                        # This file
```

## 🌐 Backend Integration

### API Endpoints Expected

#### Authentication
```
POST /api/auth/login      # Login with staff_id & password
POST /api/auth/logout     # Logout user
GET  /api/auth/me         # Get current user info
```

#### Chat
```
POST /api/chat/message    # Send message to chatbot
GET  /api/chat/history    # Get chat history
POST /api/chat/new        # Start new chat session
```

#### Documents (Optional)
```
GET  /api/documents/search  # Search documents
GET  /api/documents/{id}    # Get specific document
```

### Automatic Fallback

The app automatically falls back to mock authentication when the real backend API is not available:

1. **First attempt**: Tries your FastAPI backend at configured URL
2. **Fallback**: Uses mock authentication with the test accounts
3. **Seamless**: No additional configuration needed

## 📜 Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run lint` - Run ESLint for code quality

## 🔄 Development vs Production

### Development Mode
- Hot reload for fast development
- Source maps for debugging
- Mock responses when backend unavailable
- Detailed error messages
- Development-optimized builds

### Production Mode
- Optimized and minified builds
- Production API endpoints
- Error boundary handling
- Performance optimizations

## 🎨 Design Features

- **Professional Banking UI**: Dark theme with carefully chosen accent colors
- **Responsive Design**: Mobile-first approach with desktop enhancements
- **Accessibility**: ARIA labels and proper semantic HTML
- **Vietnamese Localization**: Complete Vietnamese language support
- **Modern CSS**: CSS Grid, Flexbox, CSS Custom Properties
- **Theme System**: Easy customization through CSS variables

## 🛠️ Customization

The app uses CSS custom properties (variables) for theming. You can customize colors, fonts, and layouts by modifying the CSS variables in `src/styles/globals.css`.

### Key CSS Variables
```css
:root {
  --primary-bg: #1a1d23;
  --secondary-bg: #252832;
  --accent-color: #0ea5e9;
  --text-primary: #ffffff;
  --text-secondary: #94a3b8;
}
```

## 🌍 Environment Variables

- `VITE_API_BASE_URL` - Backend API base URL (default: http://localhost:8000)
- `VITE_ENV` - Environment (development/production)

## 🚀 Deployment

### Build for Production

1. **Build the project**:
```bash
npm run build
# or use the build script
./build.sh
```

2. **Deploy the `dist` folder** to your web server or hosting service:
   - **Vercel**: Zero-config deployment
   - **Netlify**: Drag and drop or Git integration
   - **AWS S3 + CloudFront**: Static hosting with CDN
   - **GitHub Pages**: Free hosting for open source
   - **Traditional Server**: Upload dist folder to web root

3. **Update environment variables** for production:
```env
VITE_API_BASE_URL=https://your-production-api.com
VITE_ENV=production
```

### Production Checklist

- [ ] Update API endpoints to production URLs
- [ ] Configure CORS settings on backend
- [ ] Set up SSL certificates
- [ ] Configure domain and DNS
- [ ] Test authentication with real backend
- [ ] Monitor performance and errors

## 🔧 Troubleshooting

### Common Issues

1. **White page on load**: Check browser console for errors
2. **API connection fails**: Verify backend URL in `.env`
3. **Authentication not working**: Ensure backend endpoints match expected format
4. **Build errors**: Check Node.js version (requires 18+)

### Development Commands

```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check for outdated packages
npm outdated

# Update packages
npm update
```

## 📄 License

This project is part of a Master's thesis of Khoa Phan.

## 🤝 Contributing

This is a thesis project. For questions or suggestions, please contact the project maintainer via pqkhoa99@gmail.com.

