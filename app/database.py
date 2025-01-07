from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://chatbot_user:chatbot_user@db:5432/chatbot_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    from app.models import Base
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")


