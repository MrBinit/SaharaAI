from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from agents.custom_agent import agent_with_chat_history
import uvicorn
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.crud import create_history

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
    print(f"Received query: {query.input}, session_id: {query.session_id}")
    try:
        result = agent_with_chat_history.invoke(
            {"input": query.input},
            config={"configurable": {"session_id": query.session_id}}
        )
        if result:
            print("chatbot response generated successfully.")
            create_history(
                db, 
                query = query.input, 
                result= result['output'],
                session_id= query.session_id
            )
            return {
                "query" : query.input,
                "result": result['output'],
                "session_id" : query.session_id
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)