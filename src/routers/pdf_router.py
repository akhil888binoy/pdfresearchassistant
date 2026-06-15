
from src.schemas.pdf_schema import PDFResponse , PDFRequest
from src.database.database import get_session
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from fastapi import File, UploadFile, HTTPException
import shutil
from pathlib import Path
import uuid 
from datetime import datetime
from services.validators import DocumentValidator
from PyPDF2 import PdfReader
from src.models.chunkpdf import ChunkPDF
from src.models.pdf import PDF

pdf_router = APIRouter(
    prefix="/api/pdf",
    tags=["pdfs"]
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

doc_validator = DocumentValidator(max_size=25 * 1024 * 1024)  # 25MB limit

@pdf_router.post("/upload/single" , response_model=PDFResponse , status_code=201)
async def upload_pdf(  file : UploadFile = File(...) ,session : Session=Depends(get_session)):
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
    session.refresh(create_pdf)

    with open(file_path , "rb") as pdf_file:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            print(page)
            print(page.extract_text())

            # chunk_pdf  = ChunkPDF(
            #     id = uuid.uuid4(),
            #     pdf_id = create_pdf.id,
            # )

    return {
        "success": True,
        "original_filename": file.filename,
        "stored_filename": unique_filename,
        "content_type": file.content_type,
        "size": file.size,
        "upload_time": datetime.now(),
        "location": str(file_path)
    }
