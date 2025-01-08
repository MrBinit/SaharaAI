from sqlalchemy.orm import Session
from app.models import ChatbotHistory, SessionModel
import uuid
def create_history(db: Session, query: str, result: str, session_id: str):
    print(f"Creating history: query='{query}', result='{result}', session_id='{session_id}'")
    new_entry = ChatbotHistory(query=query, result=result, session_id = session_id)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    print("History entry created with ID: {new_entry.id}, timestamp : {new_entry.timestamp}")
    return new_entry

def get_history(db: Session, history_id: int):
    print(f"Fetching history with ID: {history_id}")
    history = db.query(ChatbotHistory).filter(ChatbotHistory.id == history_id).first()
    if history:
        print(f"History found: {history}")
    else:
        print(f"No history found for the given ID.")
    return history

def get_all_history(db: Session):
    print("Fetching al history entries.....")
    histories= db.query(ChatbotHistory).all()
    print(f"{len(histories)} history entries found")
    return histories


def truncate_message(message, length=30):
    return message if len(message) <= length else message[:length] + "..."

def get_or_create_session(db: Session, session_id: str = None):
    if session_id:
        session = db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
        if session:
            return session
        else:
            new_session = SessionModel(session_id=session_id)
            db.add(new_session)
            db.commit()
            db.refresh(new_session)
            return new_session
    else:
        session_id = str(uuid.uuid4())
        new_session = SessionModel(session_id=session_id)
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        return new_session
    


def create_history(db: Session, query: str, result: str, session_id: str):
    session = get_or_create_session(db, session_id=session_id)
    session.latest_query = truncate_message(query)
    history_entry = ChatbotHistory(
        session_id=session_id,
        query=query,
        result=result
    )
    db.add(history_entry)
    db.commit()
    db.refresh(history_entry)
    return history_entry

def list_sessions(db: Session):
    sessions = db.query(SessionModel).order_by(SessionModel.updated_at.desc()).all()
    return [
        {
            "session_id": session.session_id,
            "title": session.latest_query or "New Conversation",
            "created_at": session.created_at,
            "updated_at": session.updated_at
        }
        for session in sessions
    ]