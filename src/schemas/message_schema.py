from pydantic import BaseModel, ConfigDict,Field , UUID4
from src.schemas.pdf_schema import CitationResponse
import datetime


class QuestionRequest(BaseModel):
    conversation_id : UUID4
    question: str = Field(min_length=1 , max_length=5000)

class QuestionResponse(BaseModel):
    answer : str 
    citations: list[CitationResponse]

class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : UUID4
    role : str
    content : str
    created_at : datetime.datetime