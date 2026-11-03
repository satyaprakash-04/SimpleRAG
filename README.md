# Local RAG Application – FastAPI, LangChain, Ollama & PostgreSQL

A locally hosted Retrieval-Augmented Generation (RAG) application built with **Python, FastAPI, LangChain, Ollama, Gemma 4, Sentence Transformers, PostgreSQL, and pgvector**.

The application allows users to ingest documents, generate and store embeddings, and ask natural-language questions about their documents. It retrieves relevant information using vector similarity search and generates answers using a locally hosted LLM.

The application also supports streaming responses, allowing users to receive generated answers progressively.

## Features

- **Local LLM:** Run Gemma 4 through Ollama.
- **RAG:** Retrieve relevant document chunks before generating answers.
- **Document ingestion:** Extract and process PDF, DOCX, and other supported documents.
- **Vector storage:** Store embeddings in PostgreSQL using pgvector.
- **Semantic search:** Search documents using natural-language questions.
- **LangChain integration:** Prompt construction and LLM orchestration.
- **Streaming responses:** Stream generated answers through FastAPI.
- **Session-based conversations:** Support independent conversation histories.
- **Reusable embedding service:** Use the same embedding model for document ingestion and user queries.
- **CPU support:** Designed to support local CPU-based inference.

## Architecture

```text
                    Client
                      |
                      v
                 FastAPI
                      |
          +-----------+-----------+
          |                       |
          v                       v
      Ingestion API            Chat API
          |                       |
          v                       v
    IngestionService           ChatService
          |                       |
          v                       |
      ETL Pipeline                |
          |                       |
     +----+----+                  |
     |    |    |                  |
     v    v    v                  v
  Extract Transform Embed     RAGService
                       |          |
                       v          v
                   PostgreSQL  VectorRepository
                   + pgvector      |
                                   |
                              Retrieved Chunks
                                   |
                                   v
                              Prompt Builder
                                   |
                                   v
                              Ollama / Gemma 4
                                   |
                                   v
                              Streamed Answer
```

## Technology Stack

| Component               | Technology            |
| ----------------------- | --------------------- |
| Programming language    | Python                |
| Package manager         | uv                    |
| API framework           | FastAPI               |
| LLM                     | Gemma 4               |
| Local model runtime     | Ollama                |
| LLM orchestration       | LangChain             |
| Embedding model         | Sentence Transformers |
| Default embedding model | all-MiniLM-L6-v2      |
| Vector database         | PostgreSQL + pgvector |
| ORM                     | SQLAlchemy            |
| Database driver         | Psycopg               |
| Document processing     | PyMuPDF, python-docx  |


## Prerequisites

Install the following before running the application:

1. Python 3.11 or later.
2. [uv](https://docs.astral.sh/uv/).
3. [Docker Desktop](https://www.docker.com/products/docker-desktop/).
4. [Ollama](https://ollama.com/).
5. Git.

Verify installations:

```bash
python --version
uv --version
docker --version
ollama --version
```

## 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>

cd SimpleRAG
```

## 2. Set up the Python environment using uv

Initialize the project if you haven't already:

```bash
uv init
```

Create a virtual environment:

```bash
uv venv
```

Activate it if you want to use the environment directly.

Windows:

```powershell
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Alternatively, use `uv run` throughout the project without manually activating the environment.

### Install dependencies

Install all dependencies:

```bash
uv sync
```

## 3. Configure PostgreSQL with pgvector

The application uses PostgreSQL as its persistent storage and pgvector for vector similarity search.

### Docker Compose

```bash
docker compose up -d
```

### Enable pgvector

Connect to PostgreSQL:

```bash
docker exec -it <container_name> psql -U <postgres_username> -d <db_name>
```

Execute:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Verify:

```sql
SELECT extname FROM pg_extension;
```

## 4. Configure environment variables

Create a `.env` file in the project root. Add variables as mentioned in <code>.env.examples</code>

**Important:** The embedding dimension in your configuration must match the dimension of your database vector column.

For `all-MiniLM-L6-v2`, the embedding dimension is 384.

## 5. Set up Ollama and Gemma 4

Install Ollama from:

[https://ollama.com/](https://ollama.com/)

Pull the model:

```bash
ollama pull gemma4:e2b
```

Start the Ollama service if it is not already running:

```bash
ollama serve
```

In another terminal, verify the model:

```bash
ollama list
```

Test the model:

```bash
ollama run gemma4:e2b
```


> For a machine with 8 GB RAM and CPU-only inference, start with the smaller E2B model. Actual memory usage depends on quantization, context size, and other running processes.

## 6. Initialize the database

Create the required tables using your SQLAlchemy models or your project's migration setup.

If you are using SQLAlchemy's `Base.metadata.create_all()` during initial development, ensure all model modules have been imported before executing it.

Example:

```python
from database.connector import Base, engine

# Import models before create_all.
from app.models.document import Document
from app.models.chunk import DocumentChunkModel

Base.metadata.create_all(bind=engine)
```

For an evolving application, prefer Alembic migrations instead of relying on `create_all()`.

## 7. Run the ETL pipeline

The ETL pipeline extracts documents, cleans their contents, splits them into chunks, generates embeddings, and stores the results in PostgreSQL.

### ETL workflow

```text
PDF / DOCX
    |
    v
FileExtractor
    |
    v
TextCleaner
    |
    v
DocumentTransformer
    |
    v
DocumentChunker
    |
    v
DocumentEmbedder
    |
    v
PostgresLoader
    |
    v
PostgreSQL + pgvector
```

### Add documents

Place your documents inside:

```text
datasource/
    ├── python.pdf
    ├── machine_learning.pdf
    └── data_engineering.pdf
```

### Run the pipeline using uv

Update the manage_process.py and run it `uv run manage_process.py`.


## 8. Run the FastAPI application

Once the database, embedding model, and Ollama are ready, start the application.

```bash
uv run uvicorn app.main:app --reload
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```


## 9. Query documents using natural language

The RAG process follows these steps:

1. Accept the user's natural-language question.
2. Generate an embedding using the same model used during ingestion.
3. Retrieve relevant chunks from PostgreSQL using pgvector.
4. Construct a context-aware prompt using LangChain.
5. Send the prompt to Ollama.
6. Generate an answer using Gemma 4.

### Example request

```http
POST /chat/stream
Content-Type: application/json
```

```json
{
    "question": "Explain polymorphism in Python."
}
```

Example cURL:

```bash
curl -N -X POST "http://127.0.0.1:8000/chat/stream" \
    -H "Content-Type: application/json" \
    -d "{\"question\":\"Explain polymorphism in Python\"}"
```

The generated answer is streamed progressively to the client.

## 10. Context window and retrieval configuration

The context window determines how much information the LLM can process in one request.

The available context is shared among:

- System instructions.
- Retrieved document chunks.
- Conversation history.
- Current user question.
- Generated answer.

Initial recommended configuration:

| Parameter             |          Value |
| --------------------- | -------------: |
| Context window        |    4096 tokens |
| Retrieval top_k       |              5 |
| Chunk size            | 500–800 tokens |
| Chunk overlap         |  75–100 tokens |
| Maximum output tokens |            512 |

These are initial values and should be tuned based on the model's memory requirements and retrieval quality.

Future improvements can include:

- Maximum Marginal Relevance (MMR).
- Reranking retrieved chunks.
- Token-aware context management.
- Conversation history management.
- Source attribution and citations.
- Metadata-based document filtering.

## 11. Useful uv commands

| Command                     | Description                |
| --------------------------- | -------------------------- |
| `uv init`                   | Initialize a project       |
| `uv venv`                   | Create virtual environment |
| `uv add package-name`       | Add a dependency           |
| `uv add --dev package-name` | Add development dependency |
| `uv sync`                   | Synchronize dependencies   |
| `uv lock`                   | Update lockfile            |
| `uv run python script.py`   | Run Python script          |
| `uv run pytest`             | Run tests                  |
| `uv run ruff check .`       | Run linting                |
| `uv tree`                   | Display dependency tree    |


## 13. Development Roadmap

- [x] Document extraction.
- [x] Text cleaning and chunking.
- [x] Local embedding generation.
- [x] Store embeddings in PostgreSQL with pgvector.
- [x] Natural-language retrieval.
- [x] LangChain integration.
- [x] Ollama and Gemma 4 integration.
- [x] Streaming LLM responses.
- [ ] Conversation history and session isolation.
- [ ] Token-aware context management.
- [ ] Reranking and improved retrieval.
- [ ] Source citations in streamed responses.
- [ ] Background ingestion workers.
- [ ] Authentication and authorization.
- [ ] RAG evaluation and monitoring.

## 14. Important Design Principles

1. Use the same embedding model for document ingestion and user queries.
2. Keep ETL, retrieval, prompt construction, and LLM generation separate.
3. Reuse heavyweight model instances instead of loading them per request.
4. Keep conversation memory separate from document knowledge.
5. Use token-aware context management to avoid exceeding the model's context window.
6. Use database transactions and proper rollback handling during ingestion.
7. Keep the application local and avoid sending private document content to external LLM services.

---

## Quick Start

Once everything is configured, the typical workflow is:

**Terminal 1 – Start PostgreSQL**

```bash
docker compose up -d postgres
```

**Terminal 2 – Start Ollama**

```bash
ollama serve
```

**Terminal 3 – Ingest documents**

```bash
uv run python manage_process.py
```

**Terminal 4 – Start FastAPI**

```bash
uv run uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Your local RAG application is ready to accept natural-language questions about the ingested documents.

---

## License

Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/
