from pydantic import BaseModel, ConfigDict,Field
from uuid import UUID
from pdf_schema import CitationResponse
import datetime


class QuestionRequest(BaseModel):
    question: str = Field(min_length=1 , max_length=5000)

class QuestionResponse(BaseModel):
    answer : str 
    citations: list[CitationResponse]

class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : UUID
    role : str
    content : str
    created_at : datetime.datetime