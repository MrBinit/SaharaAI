from sqlalchemy.orm import Session
from app.models import ChatbotHistory

def create_history(db: Session, query: str, result: str, session_id: str):
    print(f"Creating history: query='{query}', result='{result}', session_id='{session_id}'")
    new_entry = ChatbotHistory(query=query, result=result)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    print("History entry created with ID: {new_entry.id}")
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
