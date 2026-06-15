from pydantic import BaseModel, ConfigDict,Field
from uuid import UUID
import datetime

class ChunkResponse(BaseModel):
    id : UUID
    pdf_id : UUID
    page_number : int 
    chunk_text: str
    created_at : datetime.datetime