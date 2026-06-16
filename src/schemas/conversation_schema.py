from pydantic import BaseModel, ConfigDict,Field 
import datetime
import uuid

class ConversationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : uuid.UUID
    created_at : datetime.datetime