# api/index.py
from fastapi import FastAPI, File, UploadFile, Depends
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    
    # Save the file
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(await file.read())
    
    # Save file info to database
    new_pdf = models.PDF(filename=file.filename, path=file_location)
    db.add(new_pdf)
    db.commit()
    db.refresh(new_pdf)
    
    return {"filename": file.filename, "message": "PDF uploaded successfully"}

@app.get("/")
async def root():
    return {"message": "Hello World"}