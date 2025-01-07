from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ChatbotHistory(Base):
    __tablename__   = "chatbot_history"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, nullable=False)
    query = Column(String, nullable=False)
    result = Column(String, nullable=False)

print("Model `ChatbotHistory` loaded successfully.")
    