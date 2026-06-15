

from src.database.database import Base
from sqlalchemy import Column,TIMESTAMP
from uuid import UUID

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID , primary_key=True , nullable=False)
    created_at = Column(TIMESTAMP , nullable=False)
