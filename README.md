# PAKS — Personal AI Knowledge System

> A production-grade Retrieval-Augmented Generation (RAG) application that lets you chat with your own documents using Claude LLM.

![Python](https://img.shields.io/badge/Python-3.13-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.136-green?style=flat-square)
![Next.js](https://img.shields.io/badge/Next.js-16-black?style=flat-square)
![ChromaDB](https://img.shields.io/badge/ChromaDB-1.5-orange?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-Compose-blue?style=flat-square)
![Claude](https://img.shields.io/badge/Claude-Anthropic-purple?style=flat-square)

---

## What is PAKS?

PAKS turns your documents into a searchable AI knowledge base. Upload any text document, and Claude will answer questions based exclusively on your content — not its general training data.

```
You: "What does my research paper say about optimizers?"

PAKS: "Based on your paper (research.pdf), Adam optimizer
       converges faster than SGD in your experiments,
       with a learning rate of 0.001..."
```

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Next.js Frontend                   │
│         Chat UI · Document Upload · Sessions         │
└────────────────────┬────────────────────────────────┘
                     │ HTTP
┌────────────────────▼────────────────────────────────┐
│                  FastAPI Backend                      │
│    Ingest · Query · Chat · Research Routers          │
└──────┬──────────────┬───────────────────┬───────────┘
       │              │                   │
┌──────▼──────┐ ┌─────▼──────┐ ┌────────▼────────┐
│   Chunker   │ │  Embedder  │ │   LLM Service   │
│ 200w chunks │ │sentence-   │ │  Anthropic      │
│ 50w overlap │ │transformers│ │  Claude API     │
└──────┬──────┘ └─────┬──────┘ └────────▲────────┘
       │              │                  │
       └──────┬───────┘                  │
       ┌──────▼──────────────────────────┴───────┐
       │              ChromaDB                    │
       │   Vector Store · Cosine Similarity       │
       └─────────────────────────────────────────┘
```

---

## Features

- **Document Ingestion** — Upload text documents, automatically chunked and embedded
- **Semantic Search** — Cosine similarity search over vector embeddings
- **RAG Pipeline** — Retrieved chunks injected as context into Claude's prompt
- **Conversation Memory** — Multi-turn chat with full history per session
- **REST API** — Clean FastAPI endpoints with Pydantic validation
- **Modern UI** — Dark-themed Next.js frontend with real-time chat
- **Docker Ready** — Single command deployment with Docker Compose

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Anthropic Claude (claude-haiku-4-5) |
| Vector DB | ChromaDB with cosine similarity |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Backend | FastAPI, Python 3.13, Pydantic |
| Frontend | Next.js 16, TypeScript, React |
| Deployment | Docker, Docker Compose |
| Monitoring | Datadog (production) |

---

## Project Structure

```
Project-/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── core/
│   │   └── config.py            # Environment configuration
│   ├── models/
│   │   └── schemas.py           # Pydantic request/response models
│   ├── routers/
│   │   ├── ingest.py            # Document ingestion endpoints
│   │   ├── query.py             # RAG search endpoint
│   │   ├── chat.py              # Multi-turn chat endpoint
│   │   └── research.py          # Research tracker
│   ├── services/
│   │   ├── chunker.py           # Text chunking (200w, 50w overlap)
│   │   ├── embedder.py          # Sentence transformer embeddings
│   │   ├── vector_store.py      # ChromaDB wrapper
│   │   ├── ingest_service.py    # Ingestion orchestrator
│   │   ├── query_service.py     # RAG query orchestrator
│   │   ├── chat_service.py      # Chat with memory
│   │   └── llm.py              # Anthropic Claude wrapper
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── page.tsx             # Main chat UI
│   │   └── layout.tsx
│   ├── lib/
│   │   └── api.ts               # FastAPI client
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.13+
- Node.js 20+
- Docker Desktop
- Anthropic API key → [console.anthropic.com](https://console.anthropic.com)

### Option 1 — Docker (Recommended)

```bash
# Clone the repo
git clone https://github.com/amiya2001/Project-.git
cd Project-

# Add your API key
echo "ANTHROPIC_API_KEY=your-key-here" > backend/.env

# Start everything
docker-compose up --build
```

Open `http://localhost:3000`

### Option 2 — Local Development

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=your-key-here" > .env
fastapi dev main.py

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/ingest/` | Ingest a document |
| `GET` | `/api/ingest/documents` | List all documents |
| `POST` | `/api/query/search` | RAG search query |
| `POST` | `/api/chat/` | Multi-turn chat |
| `DELETE` | `/api/chat/{session_id}` | Clear chat session |
| `GET` | `/health` | Health check |

### Example — Ingest a document

```bash
curl -X POST http://localhost:8000/api/ingest/ \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "my_notes.txt",
    "content": "RAG stands for Retrieval Augmented Generation...",
    "tags": ["AI", "RAG"]
  }'
```

Response:
```json
{
  "filename": "my_notes.txt",
  "status": "success",
  "chunks_created": 3
}
```

### Example — Chat

```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session_1",
    "message": "What is RAG?",
    "top_k": 3
  }'
```

Response:
```json
{
  "session_id": "session_1",
  "answer": "Based on your documents, RAG stands for...",
  "turn": 1
}
```

---

## How RAG Works

```
1. INGEST
   Document → Chunker (200 words, 50 overlap)
            → Embedder (384-dim vectors)
            → ChromaDB (persistent storage)

2. QUERY
   Question → Embed query
            → ChromaDB cosine similarity search
            → Top-k chunks retrieved

3. GENERATE
   Question + Chunks → Claude prompt
                     → "Answer only from context"
                     → Grounded response with citations
```

---

## Author

**Amiya Palai**
- Associate Developer at Cognizant
- MTech AI/ML — BITS Pilani
- AWS Certified ML Engineer
- GitHub: [@amiya2001](https://github.com/amiya2001)
- LinkedIn: [amiya-palai](https://www.linkedin.com/in/amiya-palai-740b75208/)

---

## License

MIT License — feel free to use this project as a reference or starting point.