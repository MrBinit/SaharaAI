from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from agents.custom_agent import agent_with_chat_history
import uvicorn
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.crud import create_history,  list_sessions, get_or_create_session
from translation.translation_model import translate_by_sentence
import re


app = FastAPI(title="SaharaAI")

class query(BaseModel):
    input: str
    session_id:str= "test-session"

def get_db():
    db = SessionLocal()
    try:
        print("Database session created")
        yield db
    finally:
        print("Database session closed")
        db.close()

@app.on_event("startup")
def startup_event():
    print("Starting up the application")
    init_db()
    print("application started successfully")


@app.post("/ask/")
def ask_question(query: query, db: Session = Depends(get_db)):
    try:
        normalize_input = query.input.lower()
        session = get_or_create_session(db, session_id = query.session_id)
        # to identify nepali language
        if re.search(r'[\u0900-\u097F]',normalize_input):
            print("Detected Nepali text. ")
            translated_text = translate_by_sentence(normalize_input, src_lang = "npi_Deva", tgt_lang = "eng_Latn")
            print(f"Translated Nepali to English: {translated_text}")

            result = agent_with_chat_history.invoke(
                {"input": translated_text},
                config={"configurable": {"session_id": query.session_id}}
            )
            if result:
                print("chatbot response generated successfully.")
                translated_result = translate_by_sentence(result['output'], src_lang = "eng_Latn", tgt_lang = "npi_Deva")
                history_entry = create_history(
                    db, 
                    query = query.input, 
                    result= translated_result,
                    session_id= query.session_id
                )
                return {
                    "query" : query.input,
                    "result": translated_result,
                    "session_id" : query.session_id,
                    "timestamp": history_entry.timestamp  
                }
            else:
                print("No result found for query")
                raise HTTPException(status_code=500, detail="No result found")
        else:
            print("Detected English text")
            result = agent_with_chat_history.invoke(
            {"input": query.input},
            config={"configurable": {"session_id": query.session_id}}
        )
            if result:
                print("chatbot response generated successfully.")
                history_entry = create_history(
                    db, 
                    query = query.input, 
                    result= result['output'],
                    session_id= query.session_id
                )
                return {
                    "query" : query.input,
                    "result": result['output'],
                    "session_id" : query.session_id,
                    "timestamp": history_entry.timestamp  
                }
            else:
                print("No result found for query")
                raise HTTPException(status_code=500, detail="No result found")
                
    except Exception as e:
        print("Exception occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/")
def root():
    return {"message": "Welcome to Sahara AI!"}


@app.get("/sessions/")
def get_sessions(db: Session = Depends(get_db)):
    return list_sessions(db)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)