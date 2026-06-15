from pydantic import BaseModel, ConfigDict,Field
from uuid import UUID
import datetime


class PDFRequest(BaseModel):
    filename:str
    
class PDFResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : UUID
    filename:str
    created_at : datetime.datetime

class CitationResponse(BaseModel):
    pdf_name : str 
    page_number : int
    chunk_id : UUID