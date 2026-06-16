

from src.database.database import Base
from sqlalchemy import Column, String,  TIMESTAMP, text, ForeignKey  , UUID

class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID , primary_key=True , nullable=False)
    conversation_id = Column(UUID, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    role = Column(String , nullable=False)
    content = Column(String , nullable=False)
    created_at = Column(TIMESTAMP , nullable=False)
