# Vietnam Legal Chatbot

A comprehensive legal assistant chatbot for Vietnamese law, built with retrieval-augmented generation (RAG) technology. This system helps users find and understand Vietnamese legal documents through natural language interactions.

## 🎯 Project Overview

This project provides an intelligent chatbot that can:
- Search through Vietnamese legal documents semantically
- Provide accurate answers based on official legal sources
- Track relationships between different legal documents
- Offer conversational interface for legal queries

## 🏗️ Architecture

The system implements a modern RAG (Retrieval-Augmented Generation) architecture with:

- **FastAPI Backend**: RESTful API for chatbot interactions
- **Vector Database**: Qdrant for semantic document search
- **Graph Database**: Neo4j for legal document relationships
- **Document Processing**: Advanced chunking and embedding pipeline
- **LLM Integration**: OpenAI API for natural language generation

## 📁 Project Structure

```
vietnam-law-chatbot/
├── README.md                       # README
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
└── app/                            # Main application
    ├── requirements.txt            # Python dependencies
    └── backend/                    # Backend service code
        ├── main.py                 # FastAPI application entry point
        ├── core/                   # Core configurations and prompts
        │   ├── config.py           # Application settings
        │   └── prompts.py          # LLM system prompts
        ├── retrieval/              # Document retrieval system
        │   ├── document_stores/    # Qdrant integration
        │   ├── embedders/          # Text embedding models
        │   ├── retrievers/         # Document retrieval logic
        │   └── indexing/           # Document processing pipeline
        │       ├── crawler.py      # VBPL document crawler
        │       └── chunking.py     # Document chunking
        ├── chunking/               # Processed document storage
        ├── data/                   # Raw and processed data
        └── test/                   # Testing and utilities
```

## ✨ Key Features

- **🔍 Intelligent Document Search**: Semantic search through Vietnamese legal documents using vector embeddings
- **📄 Document Crawling**: Automated extraction from VBPL (Vietnam Government Portal)
- **🧠 Smart Chunking**: AI-powered document segmentation for better retrieval
- **🔗 Relationship Mapping**: Graph-based tracking of legal document relationships
- **💬 Natural Conversations**: Chat interface for legal queries in Vietnamese
- **📊 Multiple Retrieval Strategies**: Hybrid search combining dense and sparse embeddings

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Neo4j database (local or cloud)
- Qdrant vector database (local or cloud)
- OpenAI API key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pqkhoa99/vietnam-law-chatbot.git
   cd vietnam-law-chatbot
   ```

2. **Set up environment:**
   ```bash
   # Copy environment template
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Navigate to app directory:**
   ```bash
   cd app
   ```

4. **Install dependencies:**
   ```bash
   # Using pip
   pip install -r requirements.txt
   
   # Or using uv (recommended for faster installation)
   pip install uv
   uv pip install -r requirements.txt
   ```

5. **Start the application:**
   ```bash
   # Development mode with auto-reload
   python -m uvicorn backend.main:app --reload
   
   # Or simple start
   python -m backend.main
   ```

6. **Access the API:**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs

## 🔄 Data Processing Pipeline

The system processes legal documents through several stages:

1. **📥 Document Crawling**
   ```bash
   # Crawl documents by category
   python -m backend.retrieval.indexing.crawler
   ```

2. **✂️ Document Chunking**
   ```bash
   # Process and chunk documents
   python -m backend.test.indexing [document_id]
   ```

3. **🔍 Indexing & Embedding**
   - Converts text to vector embeddings
   - Stores in Qdrant for semantic search

4. **🕸️ Relationship Extraction**
   - Identifies connections between legal documents
   - Builds knowledge graph in Neo4j

## 🛠️ Development

### Testing Document Processing

```bash
cd app

# Test document crawling and chunking
python -m backend.test.indexing [document_id]

# Test retrieval functionality
python -m backend.test.retrieval_utils
```

### Available Scripts

- `python -m backend.main` - Start the FastAPI server
- `python -m backend.test.indexing` - Test document processing
- `python -m backend.test.crawl_thongtu` - Test document crawling

## 📚 Documentation

- **Backend API**: See `app/backend/README.md` for detailed backend documentation
- **API Docs**: Available at http://localhost:8000/docs when running
- **Configuration**: Check `.env.example` for environment variables

## 🔄 CI/CD

![CI](https://github.com/pqkhoa99/vietnam-law-chatbot/workflows/CI/badge.svg)

Automated testing runs on every push and pull request:
- **Python 3.11** compatibility testing
- **Code linting** with flake8 for syntax errors
- **Import validation** for core modules
- **FastAPI app** startup verification

## 🤝 Contributing

This project is part of a Master's thesis. For questions or collaboration:

**Author**: Khoa Phan  
**Email**: pqkhoa99@gmail.com  
**Repository**: https://github.com/pqkhoa99/vietnam-law-chatbot

## 📄 License

This project is developed as part of academic research. Please contact the author for usage rights and licensing information.

---