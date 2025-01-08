from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class ChatbotHistory(Base):
    __tablename__   = "chatbot_history"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, nullable=False)
    query = Column(String, nullable=False)
    result = Column(String, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class SessionModel(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.session_id"),unique=True, nullable=False)
    latest_query = Column(String, nullable=True) 
    created_at = Column(DateTime, default = lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

print("Model `ChatbotHistory` loaded successfully.")
    