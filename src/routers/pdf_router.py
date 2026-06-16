
from src.schemas.pdf_schema import PDFResponse , PDFRequest
from src.schemas.message_schema import QuestionResponse , QuestionRequest
from src.schemas.message_schema import MessageResponse
from src.schemas.conversation_schema import ConversationResponse
from src.database.database import get_session
from src.models.conversation import Conversation
from src.models.message import Message
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from fastapi import File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
import shutil
from pathlib import Path
import uuid 
from datetime import datetime
from src.services.validators import DocumentValidator
from pypdf import PdfReader
from src.models.chunkpdf import ChunkPDF
from src.models.pdf import PDF
import chromadb
from ollama import chat
from ollama import ChatResponse



chroma_client = chromadb.PersistentClient('chroma_db')
collections = chroma_client.get_or_create_collection(name="pdfresearchassistant")

pdf_router = APIRouter(
    prefix="/api/pdf",
    tags=["pdfs"]
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

doc_validator = DocumentValidator(max_size=25 * 1024 * 1024)  # 25MB limit

def splitter(n, s):
    pieces = s.split()
    return (" ".join(pieces[i:i+n]) for i in range(0, len(pieces), n))


@pdf_router.post("/upload/single" , response_model=PDFResponse, status_code=201)
async def upload_pdf(  file : UploadFile = File(...) , session : Session=Depends(get_session)):
    """Upload a single file with basic validation"""
    validation = await doc_validator.validate_file(file)

    if not validation["valid"]:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "File validation failed",
                "errors": validation["errors"]
            }
        )

    file_ext = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file: {str(e)}"
        )
    
    create_pdf = PDF(
        id = uuid.uuid4(),
        filename = unique_filename,
        created_at = datetime.now()
    )
    session.add(create_pdf)
    session.commit()
    with open(file_path , "rb") as pdf_file:
        reader = PdfReader(pdf_file)
        chunk_number = 0 
        for page in reader.pages:
            for piece in splitter(200, page.extract_text()):
                    chunk_pdf  = ChunkPDF(
                        id = uuid.uuid4(),
                        pdf_id = create_pdf.id,
                        chunk_text = piece,
                        page_number = page.page_number,
                        chunk_number = chunk_number
                    )
                    collections.add(
                        ids=[str(chunk_pdf.id)],
                        documents=[piece],
                        metadatas=[{
                            "pdf_id" : str(create_pdf.id),
                            "page_number": chunk_pdf.page_number,
                            "chunk_number": chunk_number
                        }]
                    )
                    chunk_number = chunk_number+1
                    session.add(chunk_pdf)

    session.commit()
                    
    return PDFResponse(
        id = create_pdf.id,
        filename= create_pdf.filename,
        created_at= create_pdf.created_at
    )

    # return {
    #     "success": True,
    #     "original_filename": file.filename,
    #     "stored_filename": unique_filename,
    #     "content_type": file.content_type,
    #     "size": file.size,
    #     "upload_time": datetime.now(),
    #     "location": str(file_path)
    # }


@pdf_router.post("/conversation" , status_code=201)
async def create_conversation( session : Session = Depends(get_session)):
     conversaiton = Conversation(
          id = uuid.uuid4(),
          created_at = datetime.now()
     )
     session.add(conversaiton)
     session.commit()
     return{
          "conversation" : conversaiton.id
     }

@pdf_router.get("/conversations" ,response_model = list[ConversationResponse], status_code=201)
async def get_conversations( session : Session = Depends(get_session) ):
    stmt = session.query(Conversation)
    conversations = session.scalars(stmt).all()
    return[ConversationResponse.model_validate(conversation) for conversation in conversations]

@pdf_router.get("/messages/{conversation_id}" , response_model= list[MessageResponse] ,  status_code=201)
async def get_messages ( conversation_id : str , session : Session= Depends(get_session)):
    stmt = session.query(Message).where(Message.conversation_id == conversation_id )
    messages = session.scalars(stmt).all()
    return[MessageResponse.model_validate(message) for message in messages]

@pdf_router.post("/query" ,  status_code=201)
async def get_query( question_request : QuestionRequest , session : Session = Depends(get_session)):
        collc = collections.query(
            query_texts=[str(question_request.question)],
            n_results=5,
            include=["documents", "metadatas", "distances"],
        )
        retrieved_documents = collc.get("documents", [[]])[0]
        retrieved_metadatas = collc.get("metadatas", [[]])[0]
        message_request = Message(
             id = uuid.uuid4(),
             conversation_id = question_request.conversation_id,
             role = 'user',
             content = question_request.question,
             created_at = datetime.now()
        )
        session.add(message_request)
        prompt=f"You are a helpful research assistant. Use only the provided context to answer. Context {retrieved_documents} . Question {question_request.question}"
        response : ChatResponse = chat(model='gemma3' , messages=[
             {
                  'role' : 'user',
                  'content' : prompt
             }
        ])
        message_response = Message(
            id = uuid.uuid4(),
            conversation_id = question_request.conversation_id,
            role = 'assistant',
            content = response.message.content,
            created_at = datetime.now()
        )
        session.add(message_response)
        session.commit()
        return {
            "response" : response.message.content,
            "retrieval_trace": [
                {
                    "snippet": document,
                    "metadata": metadata,
                }
                for document, metadata in zip(retrieved_documents, retrieved_metadatas)
            ],
        }


@pdf_router.get("/upload/test", response_class=HTMLResponse)
async def upload_test_page():
    return """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>PDF Upload Test</title>
        <style>
          body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            margin: 40px;
            max-width: 720px;
            line-height: 1.5;
            background: #f8fafc;
          }
          .card {
            border: 1px solid #d0d7de;
            border-radius: 12px;
            padding: 20px;
            background: #fff;
          }
          label, button {
            display: block;
            margin-top: 16px;
          }
          button {
            padding: 10px 14px;
            border: 0;
            border-radius: 8px;
            background: #111827;
            color: white;
            cursor: pointer;
          }
          pre {
            margin-top: 16px;
            padding: 12px;
            background: #f6f8fa;
            border-radius: 8px;
            overflow: auto;
          }
        </style>
      </head>
      <body>
        <div class="card">
          <h1>PDF Upload Test</h1>
          <p>Select a PDF and send it to <code>/api/pdf/upload/single</code>.</p>

          <label for="file">PDF file</label>
          <input id="file" type="file" accept="application/pdf" />
          <button id="send">Upload</button>

          <pre id="output">Idle.</pre>
        </div>

        <script>
          const fileInput = document.getElementById("file");
          const sendButton = document.getElementById("send");
          const output = document.getElementById("output");

          sendButton.addEventListener("click", async () => {
            const file = fileInput.files[0];

            if (!file) {
              output.textContent = "Choose a PDF first.";
              return;
            }

            const formData = new FormData();
            formData.append("file", file);

            output.textContent = "Uploading...";

            try {
              const response = await fetch("/api/pdf/upload/single", {
                method: "POST",
                body: formData
              });

              const text = await response.text();
              output.textContent = `Status: ${response.status}\\n\\n${text}`;
            } catch (error) {
              output.textContent = `Request failed: ${error.message}`;
            }
          });
        </script>
      </body>
    </html>
    """
