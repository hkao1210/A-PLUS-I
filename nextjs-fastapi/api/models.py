from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class PDF(Base):
    __tablename__ = "pdfs"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    path = Column(String)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())