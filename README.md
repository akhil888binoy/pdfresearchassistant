# PDF Research Assistant

FastAPI app for PDF question answering with a retrieval-augmented generation pipeline:

1. Upload a PDF
2. Split it into chunks
3. Store chunks in Chroma
4. Retrieve relevant context on query
5. Generate an answer with Ollama

The app includes a dummy frontend at `/` that exercises the backend APIs and shows the retrieved chunks used for each answer.

## RAG Architecture

This project is not a plain chat app. It uses RAG:

- `Retrieval` - uploaded PDFs are split into chunks and stored in Chroma
- `Augmentation` - the top matching chunks are inserted into the prompt
- `Generation` - Ollama generates the final answer from that grounded context

That means responses are intended to be based on the uploaded documents, not general model memory alone.

## Features

- PDF upload with basic validation
- Conversation creation and message history
- Retrieval-augmented question answering
- Persistent Chroma collection for embeddings and search
- Lightweight browser UI for testing the full flow

## Requirements

- Python 3.14+
- Ollama installed and running locally
- A model named `gemma3` available in Ollama
- A valid database connection string in `DATABASE_URL`

## Setup

```bash
uv sync
```

Create a `.env` file if needed:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/pdfresearchassistant
DEBUG=true
```

If you do not want debug mode, omit `DEBUG` or set it to `false`.

## Run

```bash
uv run uvicorn main:app --reload
```

Open the app in your browser at:

- `http://127.0.0.1:8000/` for the dummy frontend
- `http://127.0.0.1:8000/docs` for the FastAPI docs

## How It Works

### Upload Flow

`POST /api/pdf/upload/single`

- Validates the uploaded PDF
- Stores it under `uploads/`
- Extracts text from each page
- Splits text into chunks of about 200 words
- Inserts chunks into Chroma with page and chunk metadata
- Stores PDF and chunk records in the database

### Query Flow

`POST /api/pdf/query`

- Accepts a `conversation_id` and a `question`
- Retrieves the top matching chunks from Chroma
- Builds a prompt that includes the retrieved context
- Sends the prompt to Ollama
- Stores both the user question and assistant response in the database
- Returns the answer plus a retrieval trace

### Why This Is RAG

The query flow retrieves relevant document chunks before calling the LLM. The model answers using that retrieved context, which is the core RAG pattern.

## API Endpoints

Base path: `/api/pdf`

- `POST /upload/single` - upload a PDF
- `POST /conversation` - create a conversation
- `GET /conversations` - list conversations
- `GET /messages/{conversation_id}` - list messages for a conversation
- `POST /query` - ask a grounded question against retrieved chunks
- `GET /upload/test` - simple upload test page

## Storage

- Uploaded files: `uploads/`
- Chroma persistence: `chroma_db/`
- Legacy Chroma data may also exist in `chroma/`

## Notes

- The frontend at `/` is intentionally dummy and focused on API wiring.
- The app expects Ollama to be reachable from the local machine.
- If retrieval returns unexpected results, check that your PDF actually contains extractable text.
