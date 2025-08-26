# Vietnam Legal Chatbot

A full-stack RAG-powered legal assistant for Vietnamese law documents featuring a React frontend and FastAPI backend with semantic search and natural language interactions.

## 🎯 Project Overview

This is a comprehensive legal AI chatbot system designed for Vietnamese legal documents, built as part of a Master's thesis. The system combines modern web technologies with advanced AI to provide accurate legal assistance through natural language interactions.

## 🏗️ Architecture

- **Frontend**: React + Vite with professional banking-style UI
- **Backend**: FastAPI with RAG pipeline architecture
- **Vector Database**: Qdrant for semantic document search
- **Graph Database**: Neo4j for document relationships
- **AI/ML**: OpenAI API integration with Haystack framework

## 📁 Project Structure

```
vietnam-law-chatbot/
├── README.md                       # This project overview
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── docker-compose.yml              # Full stack deployment
└── app/                            # Main application
    ├── frontend/                   # React + Vite frontend
    │   ├── README.md               # Frontend documentation
    │   ├── src/                    # React components & services
    │   ├── package.json            # Frontend dependencies
    │   └── ...                     # Frontend files
    └── backend/                    # FastAPI backend
        ├── README.md               # Backend documentation
        ├── main.py                 # FastAPI entry point
        ├── requirements.txt        # Python dependencies
        ├── api/                    # REST API routes
        ├── services/               # Business logic
        ├── retrieval/              # RAG pipeline
        └── ...                     # Backend files
```

## 📚 Documentation

For detailed setup and usage instructions, please refer to the component-specific documentation:

- **🖥️ Frontend Documentation**: [app/frontend/README.md](./app/frontend/README.md)
  - React + Vite setup and configuration
  - Authentication system with demo users
  - Chat interface and UI components
  - Development and deployment guides

- **🔧 Backend Documentation**: [app/backend/README.md](./app/backend/README.md)
  - FastAPI setup and configuration
  - RAG pipeline architecture
  - Database setup (Qdrant + Neo4j)
  - API endpoints and testing

## ✨ Key Features

- 🔍 **Semantic Search** - Vector-based search through Vietnamese legal documents
- 📄 **Document Processing** - Automated crawling and intelligent chunking
- 🔗 **Relationship Mapping** - Graph-based document connections
- 💬 **Chat Interface** - Professional React-based legal assistant UI
- 🔐 **Authentication** - Staff login system with demo accounts
- 📱 **Responsive Design** - Mobile and desktop optimized
- 🌓 **Theme Support** - Dark/light mode with banking-style UI

## 🚀 Quick Start

### Full Stack Deployment (Docker Compose)

1. **Clone and setup**:
```bash
git clone https://github.com/pqkhoa99/vietnam-law-chatbot.git
cd vietnam-law-chatbot
cp .env.example .env  # Edit with your API keys
```

2. **Start all services**:
```bash
docker-compose up -d
```

3. **Access the application**:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Development Setup

For development mode, please follow the setup instructions in the respective documentation:

1. **Backend**: Follow [app/backend/README.md](./app/backend/README.md)
2. **Frontend**: Follow [app/frontend/README.md](./app/frontend/README.md)

## 🎯 Demo & Testing

The application includes demo accounts for immediate testing:

| Staff ID | Password | Role |
|----------|----------|------|
| `admin` | `admin123` | Administrator |
| `legal01` | `legal123` | Legal Officer |
| `credit01` | `credit123` | Credit Officer |
| `demo` | `demo123` | Demo User |

Try asking legal questions like:
- "Điều kiện cho vay thế chấp là gì?"
- "Tạo checklist mở thẻ tín dụng"
- "So sánh nghị định 10/2023 và 99/2022"

## 🔄 CI/CD

![CI](https://github.com/pqkhoa99/vietnam-law-chatbot/workflows/CI/badge.svg)

Automated testing runs on every push and pull request:
- **Python 3.11** compatibility testing
- **Code linting** with flake8 for syntax errors
- **Import validation** for core modules
- **FastAPI app** startup verification
- **Frontend build** testing

## 📄 License

This project is part of a Master's thesis on Vietnamese Legal AI systems.

## 🤝 Contributing

This project is part of my Master's thesis. For questions or collaboration:

**Author**: Khoa Phan  
**Email**: pqkhoa99@gmail.com  
**University**: [HCM University of Technology]  
**Thesis**: AI-Powered Legal Assistant for Vietnamese Law Documents

---

**📋 For detailed setup instructions, please refer to the component-specific README files:**
- [Frontend Documentation](./app/frontend/README.md)
- [Backend Documentation](./app/backend/README.md)
