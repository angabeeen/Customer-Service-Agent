from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from query import get_response  # imports the shared function
import uuid


app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


chat_histories={}


class Query(BaseModel):
    message: str
    session_id: Optional[str] = None 

@app.post("/chat")



async def chat(query: Query):
    session_id=query.session_id or str(uuid.uuid4())
    if session_id not in chat_histories:
        
        chat_histories[session_id]=[]
    response=get_response(query.message, chat_histories[session_id])
    chat_histories[session_id].append((query.message, response))
    return {
        "response": response,
        "session_id": session_id
    }

    

