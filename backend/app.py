from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chatbot import get_ai_response

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

# Home route
@app.get(
    "/",
    tags=["General"],
    summary="Home Endpoint",
    description="Returns a welcome message from the AI Chatbot Backend."
)
def home():
    return {
        "message": "Welcome to the AI Chatbot Backend!"
    }

@app.get(
    "/health",
    tags=["General"],
    summary="Health Check",
    description="Checks whether the backend server is running."
)
def health():
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
def chat(request: ChatRequest):

    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    try:
        reply = get_ai_response(request.message)
        return ChatResponse(response=reply)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI service error: {str(e)}"
        )