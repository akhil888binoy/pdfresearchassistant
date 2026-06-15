from pydantic import BaseModel, ConfigDict,Field
from uuid import UUID
from message_schema import MessageResponse

class ConversationResponse(BaseModel):
    id : UUID
    messages:list[MessageResponse]