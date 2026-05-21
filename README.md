# TutorRAG
🚀 **[Live Demo](https://tutor-rag-qbdh9h7dpnaji2rhixkxsr.streamlit.app/)** | 

AI-powered educational RAG platform that enables students and teachers to upload PDFs, perform semantic search, generate citation-aware answers, and create AI-powered MCQs from study material.

---

## Features

- 📄 PDF upload and ingestion pipeline
- 🔍 Semantic search using vector embeddings
- 🧠 Retrieval-Augmented Generation (RAG)
- 📚 Citation-aware answers with exact PDF references
- 👨‍🏫 Separate teacher and student workflows
- 📝 Dynamic MCQ quiz generation
- ⚡ Low-latency response generation using Groq API
- 🗂️ Metadata filtering with Pinecone
- 💬 Chat history storage with MongoDB
- ☁️ Cloud deployment using Render and Streamlit

---

## Tech Stack

### Backend
- FastAPI
- Python

### Frontend
- Streamlit

### AI / RAG
- Groq API
- Pinecone
- Vector Embeddings

### Database
- MongoDB

### Deployment
- Render
- Streamlit Cloud

---

## System Architecture

```text
PDF Upload
    ↓
Text Extraction
    ↓
Chunking & Embeddings
    ↓
Pinecone Vector Store
    ↓
Semantic Retrieval
    ↓
Groq LLM Response Generation
    ↓
Citation-Aware Answers
