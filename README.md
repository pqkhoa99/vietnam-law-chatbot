# Vietnam Legal Chatbot

A chatbot application designed to provide accurate and accessible information about Vietnamese legal matters using retrieval-augmented generation (RAG) technology.

## Project Overview

This project aims to make Vietnamese legal information more accessible to the public through a conversational interface. The system uses advanced natural language processing techniques to understand legal queries and provide reliable, sourced answers based on Vietnamese legal documents.

## Key Features

- **Legal Document Indexing**: Automatically processes and indexes legal documents from various sources
- **Multilingual Support**: Optimized for Vietnamese language queries with additional support for English
- **Source Attribution**: Provides references to original legal texts for all information
- **Context-Aware Responses**: Understands the context of legal questions to provide relevant information

## Project Structure

- `app/backend/`: Python backend service implementing the RAG pipeline
  - `api/`: FastAPI endpoints for the application
  - `core/`: Core application configuration and settings
  - `db/`: Database integrations (Qdrant & Neo4j)
  - `indexing/`: Document processing and indexing
  - `models/`: Pydantic models and schemas
  - `pipeline/`: RAG components and LLM integration
  - `services/`: Business logic layer
  - `utils/`: Utility functions

- `app/frontend/`: User interface for interacting with the legal chatbot

- `data/`: Directory for legal document storage

## Technology Stack

- **Backend**: FastAPI, Python 3.11+
- **Vector Database**: Qdrant for semantic search 
- **Graph Database**: Neo4j for knowledge graph relationships
- **LLM Integration**: Multiple LLM providers support
- **Text Processing**: Hugging Face Transformers, Sentence Transformers
- **Document Handling**: Unstructured, PyPDF, python-docx
- **Frontend**: (To be determined)

## Getting Started

See the README in the backend directory for setup and running instructions.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under Khoa Phan - pqkhoa99@gmail.com

