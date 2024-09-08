import datetime
from io import BytesIO
from fastapi import FastAPI, File, Response, UploadFile, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models
import os
from typing import List
from pydantic import BaseModel, Field

models.Base.metadata.create_all(bind=engine)

app = FastAPI(append_slash=True)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/upload-pdf")
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    try:
        content = await file.read()
        new_id = os.urandom(16).hex()  # Generate a random 32-character hex string
        new_pdf = models.PDF(id=new_id, filename=file.filename, content=content)
        db.add(new_pdf)
        db.commit()
        db.refresh(new_pdf)
        return {"id": new_pdf.id, "filename": file.filename, "message": "PDF uploaded successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while uploading the file: {str(e)}")

class PDFInfo(BaseModel):
    id: str
    filename: str
    content: bytes | None = None  
    upload_date: datetime.datetime
    class Config:
        from_attributes = True

@app.get("/api/pdfs", response_model=List[PDFInfo])
async def list_pdfs(db: Session = Depends(get_db)):
    try:
        pdfs = db.query(models.PDF).all()
        return [
            PDFInfo(
                id=str(pdf.id), 
                filename=pdf.filename,
                upload_date=pdf.upload_date,
            )
            for pdf in pdfs
        ]
    except Exception as e:
        print(f"Error in list_pdfs: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving PDFs")
    
@app.get("/api/preview-pdf/{pdf_id}")
async def preview_pdf(pdf_id: str, db: Session = Depends(get_db)):
    pdf = db.query(models.PDF).filter(models.PDF.id == pdf_id).first()
    if not pdf:
        raise HTTPException(status_code=404, detail="PDF not found")
    
    return Response(content=pdf.content, media_type="application/pdf")

@app.get("/api/download-pdf/{pdf_id}")
async def download_pdf(pdf_id: str, db: Session = Depends(get_db)):
    pdf = db.query(models.PDF).filter(models.PDF.id == pdf_id).first()
    if not pdf:
        raise HTTPException(status_code=404, detail="PDF not found")
    return StreamingResponse(BytesIO(pdf.content), media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={pdf.filename}"})