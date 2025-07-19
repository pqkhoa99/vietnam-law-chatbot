# Vietnam Legal Chatbot

A RAG-powered legal assistant for Vietnamese law documents with semantic search and natural language interactions.

## �️ Tech Stack

- **FastAPI** - REST API backend
- **Qdrant** - Vector database for semantic search
- **OpenAI** - LLM integration and embeddings
- **Haystack** - Document processing pipeline

## 📁 Project Structure

```
vietnam-law-chatbot/
├── README.md                       # README
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
└── app/                            # Main application
    └── backend/                    # Backend service code
        ├── requirements.txt        # Python dependencies
        ├── main.py                 # FastAPI application entry point
        ├── core/                   # Core configurations and prompts
        ├── retrieval/              # Document retrieval system
        │   ├── document_stores/    # Qdrant integration
        │   ├── embedders/          # Text embedding models
        │   ├── retrievers/         # Document retrieval logic
        │   └── indexing/           # Document processing pipeline
        ├── chunking/               # Processed document storage
        ├── data/                   # Raw and processed data
        └── test/                   # Testing and utilities
```

## ✨ Features

- 🔍 **Semantic Search** - Vector-based search through Vietnamese legal documents
- 📄 **Document Processing** - Automated crawling and intelligent chunking
- 🔗 **Relationship Mapping** - Graph-based document connections
- 💬 **Natural Language** - Chat interface for legal queries

## 🚀 Quick Start

1. **Clone and setup:**
   ```bash
   git clone https://github.com/pqkhoa99/vietnam-law-chatbot.git
   cd vietnam-law-chatbot/app
   cp .env.example .env  # Edit with your API keys
   ```

2. **Install and run:**
   ```bash
   pip install -r requirements.txt
   python -m uvicorn backend.main:app --reload
   ```

3. **Access:**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

## 🔄 Usage

```bash
# Test document processing
python -m backend.test.indexing [document_id]

# Start development server
python -m uvicorn backend.main:app --reload
```

## 🤝 About

**Master's Thesis Project**  
Author: Khoa Phan (pqkhoa99@gmail.com)

![CI](https://github.com/pqkhoa99/vietnam-law-chatbot/workflows/CI/badge.svg)