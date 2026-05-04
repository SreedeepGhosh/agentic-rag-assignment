# Agentic RAG System

---

## 1. Introduction

This assignment implements a **production‑grade Agentic Retrieval‑Augmented Generation (RAG) system** that can interact with a local directory of PDF/Text documents. The system uses **local Large Language Models (LLMs)** via Ollama, a **vector database (ChromaDB)** for semantic retrieval, and a **multi‑agent reasoning architecture** to generate grounded and reliable responses.

The complete pipeline is served through a **FastAPI REST API**, monitored using **MLflow**, containerized using **Docker**, and validated through a **CI/CD pipeline with GitHub Actions**.

The system strictly avoids hallucinations and external internet usage by answering queries **only from locally ingested documents**.

---

## 2. Objectives of Assignment 1

The primary goals of this assignment are:

- Build a **local knowledge base** using embeddings and a vector database
- Implement **Retrieval‑Augmented Generation (RAG)**
- Introduce **Agentic Intelligence** using multiple reasoning agents
- Serve the pipeline via a **REST API**
- Track experiments and latency using **MLflow**
- Apply **engineering rigor** using Docker and CI/CD

---

## 3. High‑Level Architecture

```
PDF Documents
     ↓
LangChain Document Loader
     ↓
Text Chunking (500 chars, overlap 50)
     ↓
Embeddings (Ollama)
     ↓
ChromaDB Vector Store
     ↓
Retriever
     ↓
Agentic Reasoning (CrewAI)
     ↓
FastAPI API (/ask)
     ↓
MLflow Monitoring
```

---

## 4. Project Directory Structure

```
Assignment_1/
├── agentic_query.py        # Agentic RAG pipeline
├── api.py                  # FastAPI application
├── schemas.py              # Pydantic request/response schemas
├── ingest.py               # PDF ingestion and vectorization
├── query.py                # Baseline RAG pipeline (Task 1)
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker container definition
├── data/
│   └── pdfs/
│       └── INTERN PROJECT AND RESEARCH.pdf
├── vectorstore/            # ChromaDB persistent storage
└── mlruns/                 # MLflow experiment logs
```

---

## 5. Task 1 – Knowledge Base and RAG

### 5.1 Document Ingestion (`ingest.py`)

The ingestion pipeline performs the following steps:

1. Loads all PDFs from the `data/pdfs/` directory
2. Splits text into **500‑character chunks with 50‑character overlap**
3. Generates embeddings using a **local Ollama embedding model**
4. Stores embeddings persistently in **ChromaDB**

This ingestion step is executed **offline** and only needs to be re‑run when documents change.

---

### 5.2 Baseline RAG Pipeline (`query.py`)

A simple RAG baseline is implemented using LangChain’s `RetrievalQA`:

- Retrieves top‑k document chunks from ChromaDB
- Injects them into a prompt
- Returns an answer grounded strictly in local context

This implementation satisfies **Task 1** and serves as a reference point for the agentic system.

---

## 6. Task 2 – Agentic Intelligence

### 6.1 Why Agentic RAG?

While basic RAG systems can retrieve relevant text, they often struggle with:

- Multi‑topic documents
- Portfolio‑style PDFs
- Over‑strict or overly verbose responses

To solve this, an **Agentic RAG approach** is used, introducing multiple specialized reasoning agents that cooperate to generate robust outputs.

---

### 6.2 Agent Roles (`agentic_query.py`)

The agentic pipeline uses three agents orchestrated via **CrewAI**:

#### Agent 1 – Document Analyst
- Analyzes retrieved context
- Identifies document structure, entities, and themes

#### Agent 2 – Project Synthesizer
- Generates concise summaries grounded in context
- Allowed controlled inference only from retrieved content

#### Agent 3 – Validator
- Removes unsupported or hallucinated claims
- Ensures final response is fully grounded

---

### 6.3 Agentic Execution Flow

```
User Query
     ↓
Retriever (ChromaDB)
     ↓
Document Analyst
     ↓
Project Synthesizer
     ↓
Validator
     ↓
Final Grounded Answer
```

If a valid answer cannot be generated safely, the system returns:

```
"I do not know based on the provided documents."
```

---

## 7. Task 3 – Serving and Monitoring

### 7.1 FastAPI Service (`api.py`)

The agentic pipeline is exposed via a REST API.

**Endpoint**
```
POST /ask
```

**Request Body**
```json
{
  "query": "Summarize the document"
}
```

**Response**
```json
{
  "answer": "<grounded response>",
  "latency": 3.25
}
```

---

### 7.2 Pydantic Validation (`schemas.py`)

All API inputs and outputs are validated using **Pydantic models**, ensuring predictable and robust behavior.

---

### 7.3 MLflow Monitoring

Each API request is logged as an **MLflow experiment**, capturing:

- Query text
- Model identifier
- Retriever configuration
- Request latency

Logs are stored locally inside the `mlruns/` directory.

---

## 8. Task 4 – Engineering Rigor

### 8.1 Dockerization (`Dockerfile`)

The system is containerized using Docker:

- FastAPI application runs inside the container
- Ollama runs on the host to avoid large model images
- Container connects to Ollama using **host networking**

**Run command (Linux):**
```bash
docker run --network=host agentic-rag-app
```

---

### 8.2 CI/CD with GitHub Actions

A GitHub Actions workflow automatically builds the Docker image:

- Triggered on `push` to the `main` branch
- Validates Dockerfile and dependencies
- Ensures reproducible builds

Workflow file location:
```
.github/workflows/ci-docker-build.yml
```

---

## 9. Design Rationale

| Challenge | Solution |
|--------|----------|
Hallucination | Retrieval + validation agent |
Unstructured documents | Summarization agents |
Cloud dependency | Local Ollama |
Scalability | FastAPI + Docker |
Monitoring | MLflow |
Engineering rigor | CI/CD pipeline |

---

## 10. Key Learnings

- RAG alone is insufficient for complex documents
- Agentic reasoning improves reliability when properly constrained
- Local LLMs can support production‑grade systems
- Monitoring and CI/CD are essential for real‑world AI deployment

---

## 11. Conclusion

This assignment demonstrates a **complete, end‑to‑end AI system** covering ingestion, retrieval, agentic reasoning, serving, monitoring, containerization, and CI/CD.  
The final system is modular, robust, fully local, and production‑ready, satisfying all objectives of **Assignment 1**.

---
