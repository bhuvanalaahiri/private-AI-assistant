from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.llms import Ollama

app = FastAPI()

# Load model
llm = Ollama(model="llama3")

# Request format
class ChatRequest(BaseModel):
    message: str

# Response format
class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    answer = llm.invoke(req.message)
    return {"response": answer}
