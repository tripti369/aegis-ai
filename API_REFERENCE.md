# AI Chatbot Backend API

## Base URL

http://127.0.0.1:8000

---

## Home

GET /

Response

{
    "message": "Welcome to the AI Chatbot Backend!"
}

---

## Health

GET /health

Response

{
    "status": "healthy",
    "message": "Backend is running successfully!"
}

---

## Chat

POST /chat

Request

{
    "message": "Hello"
}

Response

{
    "response": "Hello! How can I help you?"
}

Error

{
    "detail": "Message cannot be empty."
}