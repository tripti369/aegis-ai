"""
Main chatbot pipeline.

This module:
- Builds the system prompt
- Maintains conversation memory
- Sends messages to the LLM
- Returns the AI response
"""

from memory import ConversationMemory
from prompts import build_messages
from config import DEFAULT_MODE
from llm import generate_response
from config import ASSISTANT_MODES

class AIChatbot:
    """
    Main AI Chatbot class.
    """

    def __init__(self, mode: str = DEFAULT_MODE):
        self.mode = mode
        self.memory = ConversationMemory()

    def chat(self, user_message: str) -> str:
        """
        Process a user message and return the AI response.
        """

        # Store user message
        self.memory.add_message("user", user_message)

        # Get conversation history
        history = self.memory.get_messages()

        # Build final messages
        messages = build_messages(
            user_message=user_message,
            history=history[:-1],   # current user message already added
            mode=self.mode
        )

        # Generate AI response
        response = generate_response(messages)

        # Save assistant response
        self.memory.add_message("assistant", response)

        return response

    def clear_memory(self):
        """
        Clear conversation history.
        """
        self.memory.clear()

    def get_history(self):
       """
       Return conversation history.
       """
       return self.memory.get_messages()


def get_mode(self):
    """
    Return the current assistant mode.
    """
    return self.mode


def set_mode(self, mode: str):
    """
    Change assistant mode.
    """

    if mode not in ASSISTANT_MODES:
        raise ValueError(f"Invalid mode: {mode}")

    self.mode = mode
# Global chatbot instance
chatbot = AIChatbot()


def get_ai_response(user_message: str) -> str:
    """
    Entry point used by the FastAPI backend.
    """
    return chatbot.chat(user_message)

def get_mode(self):
    print("get_mode() called")
    return self.mode