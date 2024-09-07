# api/index.py
import datetime
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models
import os
import uuid
from typing import List
from pydantic import BaseModel

models.Base.metadata.create_all(bind=engine)
app = FastAPI(append_slash=True)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.post("/api/upload-pdf")
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Create uploads directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
   
    # Generate a unique filename
    unique_filename = f"{uuid.uuid4()}.pdf"
    file_location = f"uploads/{unique_filename}"
   
    try:
        # Save the file
        with open(file_location, "wb+") as file_object:
            file_object.write(await file.read())
   
        # Save file info to database
        new_pdf = models.PDF(filename=file.filename, path=file_location)
        db.add(new_pdf)
        db.commit()
        db.refresh(new_pdf)
   
        return {"original_filename": file.filename, "stored_filename": unique_filename, "message": "PDF uploaded successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while uploading the file: {str(e)}")

class PDFInfo(BaseModel):
    id: int
    filename: str
    path: str
    upload_date: datetime

    class Config:
        from_attributes = True

@app.get("/api/pdfs", response_model=List[PDFInfo])
async def list_pdfs(db: Session = Depends(get_db)):
    try:
        pdfs = db.query(models.PDF).all()
        return [PDFInfo.model_validate(pdf) for pdf in pdfs]
    except Exception as e:
        print(f"Error in list_pdfs: {str(e)}")  # For debugging
        raise HTTPException(status_code=500, detail="An error occurred while retrieving PDFs")

