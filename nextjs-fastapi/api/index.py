import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import List
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models
from pydantic import BaseModel
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import uuid
    
# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Initialize DocTR model
model = ocr_predictor('db_resnet50', 'crnn_vgg16_bn', pretrained=True, assume_straight_pages=False)

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PDFResponse(BaseModel):
    id: str
    filename: str
    upload_date: datetime
    file_path: str

    class Config:
        from_attributes = True

class ProcessRequest(BaseModel):
    pdf_id: str
    question: str
    teacher_answer: str

def save_upload_file(upload_file: UploadFile) -> tuple[str, str]:
    """Save an uploaded file and return its ID and file path."""
    # Generate unique ID and filename
    file_id = str(uuid.uuid4())
    file_extension = os.path.splitext(upload_file.filename)[1]
    file_path = UPLOAD_DIR / f"{file_id}{file_extension}"
    
    # Save file
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    return file_id, str(file_path)

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF using DocTR."""
    try:
        # Load and process the PDF
        pdf_doc = DocumentFile.from_pdf(file_path)
        result = model(pdf_doc)
        
        # Extract text from all pages
        full_text = ""
        for page in result.pages:
            for block in page.blocks:
                for line in block.lines:
                    for word in line.words:
                        full_text += word.value + " "
        
        return full_text.strip()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error extracting text from PDF: {str(e)}"
        )

@app.post("/api/upload-pdf", response_model=PDFResponse)
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a PDF file and store its information."""
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )
    
    try:
        # Save file and get its ID and path
        file_id, file_path = save_upload_file(file)
        
        # Create database record
        new_pdf = models.PDF(
            id=file_id,
            filename=file.filename,
            file_path=file_path,
            upload_date=datetime.utcnow()
        )
        db.add(new_pdf)
        db.commit()
        db.refresh(new_pdf)
        
        return new_pdf
    
    except Exception as e:
        # Clean up file if database operation fails
        if 'file_path' in locals():
            Path(file_path).unlink(missing_ok=True)
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading file: {str(e)}"
        )

@app.post("/api/process-answer")
async def process_answer(
    request: ProcessRequest,
    db: Session = Depends(get_db)
):
    """Process a student's PDF answer."""
    try:
        # Get the PDF record from database
        pdf = db.query(models.PDF).filter(models.PDF.id == request.pdf_id).first()
        if not pdf:
            raise HTTPException(status_code=404, detail="PDF not found")

        # Check if file exists
        if not os.path.exists(pdf.file_path):
            raise HTTPException(
                status_code=404,
                detail="PDF file not found on server"
            )

        # Extract text from PDF
        student_answer = extract_text_from_pdf(pdf.file_path)

        # Process the answer using prompt.py
        from .prompt import mark_answer
        result = mark_answer(
            question=request.question,
            max_score=4,
            correct_answer=request.teacher_answer,
            student_answer=student_answer
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing answer: {str(e)}"
        )

@app.get("/api/pdfs", response_model=List[PDFResponse])
async def list_pdfs(db: Session = Depends(get_db)):
    """List all uploaded PDFs."""
    try:
        return db.query(models.PDF).all()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving PDFs: {str(e)}"
        )

# Clean up endpoint for development/testing
@app.delete("/api/pdfs/{pdf_id}")
async def delete_pdf(pdf_id: str, db: Session = Depends(get_db)):
    """Delete a PDF and its file."""
    pdf = db.query(models.PDF).filter(models.PDF.id == pdf_id).first()
    if not pdf:
        raise HTTPException(status_code=404, detail="PDF not found")
    
    try:
        # Delete file
        if os.path.exists(pdf.file_path):
            os.remove(pdf.file_path)
        
        # Delete database record
        db.delete(pdf)
        db.commit()
        return {"message": "PDF deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting PDF: {str(e)}"
        )