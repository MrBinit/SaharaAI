from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from custom_agent import agent_with_chat_history
import uvicorn

app = FastAPI()


class query(BaseModel):
    input: str
    session_id:str= "test-session"

@app.post("/ask/")
def ask_question(query: query):
    try:
        result = agent_with_chat_history.invoke(
            {"input": query.input},
            config={"configurable": {"session_id": query.session_id}}
        )
        if result:
            return {"output": result['output']}
        else:
            raise HTTPException(status_code=500, detail="No result found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/")
def root():
    return {"message": "Welcome to Sahara AI!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)