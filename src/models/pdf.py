
from src.database.database import Base
from sqlalchemy import Column,  String, TIMESTAMP, text , UUID

class PDF(Base):
    __tablename__ = "pdfs"
    id  = Column(UUID, primary_key=True, nullable=False)
    filename = Column(String, nullable=False)
    created_at = Column(TIMESTAMP , nullable=False)
