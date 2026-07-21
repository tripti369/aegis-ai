from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chatbot import chatbot, get_ai_response
from typing import List
from config import MODEL_NAME, MAX_HISTORY

# Create the FastAPI application
app = FastAPI(
    title="AI Chatbot Backend",
    description="""
This API powers our AI Chatbot project.

Features:
- Chat with Groq Llama 3.3
- FastAPI Backend
- Conversation Memory (Coming Soon)
- Streamlit Frontend Support
""",
    version="1.0.0",
    contact={
        "name": "Team 1",
        "email": "team1@example.com"
    }
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    mode: str
    message_count: int

# Home route
@app.get(
    "/",
    tags=["General"],
    summary="Home Endpoint",
    description="Returns a welcome message from the AI Chatbot Backend."
)
def home() -> dict:
    return {
        "message": "Welcome to the AI Chatbot Backend!"
    }

@app.get(
    "/health",
    tags=["General"],
    summary="Health Check",
    description="Checks whether the backend server is running."
)
def health() -> dict:
    return {
        "status": "healthy",
        "message": "Backend is running successfully!"
    }

@app.post(
    "/chat",
    tags=["Chat"],
    response_model=ChatResponse,
    summary="Chat with AI",
    description="Generate an AI response using Groq."
)
def chat(request: ChatRequest) -> ChatResponse:

    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    try:
        reply = get_ai_response(request.message)

        history = chatbot.get_history()

        return ChatResponse(
            response=reply,
            mode=chatbot.get_mode(),
            message_count=len(history)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI service error: {str(e)}"
        )
    
class HistoryMessage(BaseModel):
    role: str
    content: str


class HistoryResponse(BaseModel):
    history: List[HistoryMessage]
    message_count: int


@app.get(
    "/history",
    response_model=HistoryResponse,
    tags=["Conversation"]
)

def get_history() -> HistoryResponse:
    """
    Return the current conversation history.
    """

    history = chatbot.get_history()

    return {
        "history": history,
        "message_count": len(history)
    }

class ClearResponse(BaseModel):
    message: str

@app.post(
    "/clear",
    response_model=ClearResponse,
    tags=["Conversation"],
    summary="Clear Conversation",
    description="Deletes the current conversation history."
)

def clear_conversation() -> ClearResponse:
    """
    Clear the current conversation history.
    """

    chatbot.clear_memory()

    return {
        "message": "Conversation cleared successfully."
    }

class ModeRequest(BaseModel):
    mode: str


class ModeResponse(BaseModel):
    message: str
    mode: str

@app.get(
    "/mode",
    response_model=ModeResponse,
    tags=["Assistant"]
)
def get_mode():
    """
    Return the current assistant mode.
    """

    return {
        "message": "Current assistant mode",
        "mode": chatbot.get_mode()
    }

@app.post(
    "/mode",
    response_model=ModeResponse,
    tags=["Assistant"]
)
def change_mode(request: ModeRequest):
    """
    Change the assistant mode.
    """

    try:
        chatbot.set_mode(request.mode)

        return {
            "message": "Assistant mode updated successfully.",
            "mode": chatbot.get_mode()
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
class StatsResponse(BaseModel):
    model: str
    mode: str
    message_count: int
    memory_limit: int

@app.get(
    "/stats",
    response_model=StatsResponse,
    tags=["Assistant"],
    summary="Chat Statistics"
)
def get_stats():
    """
    Return chatbot statistics.
    """

    history = chatbot.get_history()

    return StatsResponse(
        model=MODEL_NAME,
        mode=chatbot.get_mode(),
        message_count=len(history),
        memory_limit=MAX_HISTORY
    )