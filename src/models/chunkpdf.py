


from src.database.database import Base
from sqlalchemy import Column, String,  TIMESTAMP, text, ForeignKey  , Integer
from uuid import UUID

class ChunkPDF(Base):
    __tablename__ = "chunkPDFs"

    id = Column(UUID , primary_key=True , nullable=False)
    pdf_id = Column(UUID, ForeignKey("pdfs.id", ondelete="CASCADE"), nullable=False)
    chunk_text = Column(String , nullable=False)
    embedding = Column(String , nullable=False)
    chunk_number = Column(Integer , nullable=False)