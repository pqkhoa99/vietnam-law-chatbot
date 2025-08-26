# Vietnam Legal Chatbot - Backend API

A FastAPI-based backend service for the Vietnamese Legal Chatbot system, featuring RAG (Retrieval-Augmented Generation) architecture with semantic search, graph-based document relationships, and LLM integration.

## 🎯 Overview

This backend provides a REST API for processing legal queries using a sophisticated RAG pipeline that combines vector search (Qdrant), graph relationships (Neo4j), and large language models to deliver accurate and contextual responses about Vietnamese legal documents.

## 🔧 Tech Stack

### Core Framework
- **FastAPI** - Modern, fast web framework for building APIs
- **Python 3.11+** - Programming language
- **Uvicorn** - ASGI server for FastAPI
- **Pydantic** - Data validation and settings management

### Databases & Storage
- **Qdrant** - Vector database for semantic document search
- **Neo4j** - Graph database for document relationships
- **JSON Files** - Document metadata and configurations

## 📁 Backend Structure

```
app/backend/
├── README.md                       # This file
├── main.py                         # FastAPI application entry point
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Container configuration
├── .dockerignore                   # Docker ignore rules
├── .gitignore                      # Git ignore rules
│
├── api/                            # API layer
│   └── routes.py                   # FastAPI route definitions
│
├── core/                           # Core configurations
│   ├── config.py                   # Application settings
│   ├── logging.py                  # Logging configuration
│   ├── prompts.py                  # LLM prompt templates
│   └── utils.py                    # Utility functions
│
├── domain/                         # Domain models
│   └── models.py                   # Pydantic data models
│
├── services/                       # Business logic services
│   ├── chat_service.py             # Main chat processing logic
│   ├── neo4j_service.py            # Graph database operations
│   ├── qdrant_service.py           # Vector database operations
│   └── synthesis_service.py        # Response synthesis logic
│
├── retrieval/                      # RAG pipeline components
│   ├── utils.py                    # Retrieval utilities
│   ├── document_stores/            # Qdrant Database integrations
│   ├── embedders/                  # Text embedding models
│   ├── retrievers/                 # Document retrieval logic
│   ├── generation/                 # Response generation
│   └── indexing/                   # Document chunking and Web crawling 
│
├── dataset/                        # Dataset storage
│
└── test/                           # Testing and utilities
    ├── indexing.py                 # Document indexing tests
    ├── pipeline.py                 # Pipeline testing
    └── retrieval_utils.py          # Retrieval testing utilities
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** (recommended)
- **pip** or **poetry** for package management
- **Qdrant** database instance
- **Neo4j** database instance
- **OpenAI API key** (for LLM and embeddings)

### Installation

1. **Navigate to backend directory**:
```bash
cd app/backend
```

2. **Create virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Environment configuration**:
```bash
# Copy environment template (if available in parent directory)
cp ../../.env.example .env

# Or create .env file with required variables:
touch .env
```

5. **Configure environment variables** in `.env`:

### Running the Backend

#### Development Mode

1. **Start the development server**:
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. **Alternative with direct Python**:
```bash
python main.py
```

#### Production Mode

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Using Docker

1. **Build the Docker image**:
```bash
docker build -t vietnam-law-chatbot-backend .
```

2. **Run the container**:
```bash
docker run -p 8000:8000 --env-file .env vietnam-law-chatbot-backend
```

### Accessing the API

- **API Base URL**: http://localhost:8000
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔗 API Endpoints

### Core Endpoints

#### Chat
```http
POST /chat
Content-Type: application/json

{
  "message": "Điều kiện cho vay thế chấp là gì?",
  "session_id": "optional_session_id"
}
```

#### Health Check
```http
GET /health
```

### Response Format

```json
{
  "response": "Detailed legal response...",
  "sources": [
    {
      "document_id": "doc_123",
      "title": "Nghị định số 10/2023/NĐ-CP",
      "relevance_score": 0.95,
      "excerpt": "Relevant text excerpt..."
    }
  ],
  "session_id": "session_uuid",
  "processing_time": 1.23
}
```

## 🏗️ Architecture

### RAG Pipeline Flow

1. **Query Processing**
   - Input validation and preprocessing
   - Query enhancement and expansion

2. **Vector Retrieval (Qdrant)**
   - Semantic similarity search
   - Document ranking by relevance
   - Initial candidate filtering

3. **Graph Enhancement (Neo4j)**
   - Relationship-based document discovery
   - Context enrichment through graph traversal
   - Authority and citation analysis

4. **Response Generation (LLM)**
   - Context-aware prompt construction
   - OpenAI API integration
   - Response synthesis and formatting

5. **Post-processing**
   - Citation extraction and validation
   - Response quality scoring
   - Logging and analytics

### Manual Testing

```bash
# Test API health
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Giải thích từ ngữ tiền mặt ở Thông tư 01/2014/TT-NHNN?"}'
```

## 📊 Monitoring & Logging

### Log Files

- **Application logs**: `logs/app.log`
- **Error logs**: Included in main log file with ERROR level
- **Access logs**: Uvicorn server logs

### Log Levels

- `DEBUG`: Detailed information for debugging
- `INFO`: General application information
- `WARNING`: Warning messages
- `ERROR`: Error conditions
- `CRITICAL`: Critical errors

### Health Monitoring

The `/health` endpoint provides:
- API status
- Database connectivity
- Service dependencies
- Response time metrics

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DEBUG_MODE` | Enable debug logging | `false` | No |
| `HOST` | Server host | `localhost` | No |
| `PORT` | Server port | `8000` | No |
| `OPENAI_API_KEY` | OpenAI API key | - | Yes |
| `QDRANT_URL` | Qdrant database URL | `http://localhost:6333` | Yes |
| `QDRANT_API_KEY` | Qdrant API key | - | No |
| `NEO4J_URI` | Neo4j database URI | `bolt://localhost:7687` | Yes |
| `NEO4J_USERNAME` | Neo4j username | `neo4j` | Yes |
| `NEO4J_PASSWORD` | Neo4j password | - | Yes |
| `LOG_LEVEL` | Logging level | `INFO` | No |

### Database Configuration

#### Qdrant Setup
```bash
# Using Docker
docker run -p 6333:6333 qdrant/qdrant

# Or install locally
# Follow Qdrant installation guide
```

#### Neo4j Setup
```bash
# Using Docker
docker run -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your_password \
  neo4j:latest

# Or install locally
# Follow Neo4j installation guide
```

### Debug Mode

Enable debug mode for detailed logging:
```bash
export DEBUG_MODE=true
python -m uvicorn main:app --reload
```

## 📄 License

This project is part of a Master's thesis of Khoa Phan.

## 🤝 Contributing

This is a thesis project. For questions or suggestions, please contact the project maintainer via pqkhoa99@gmail.com.