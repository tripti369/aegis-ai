"""
Conversation Memory for the AI Chatbot.

This module is responsible for:
- Storing conversation history
- Retrieving previous messages
- Clearing memory
- Limiting memory size
"""

from config import MAX_HISTORY


class ConversationMemory:
    """
    Stores conversation history in memory.
    """

    def __init__(self):
        self.messages = []

    def add_message(self, role: str, content: str):
        """
        Add a new message to memory.
        """

        self.messages.append({
            "role": role,
            "content": content
        })

        # Keep only the latest messages
        self.messages = self.messages[-MAX_HISTORY:]

    def get_messages(self):
        """
        Return a copy of conversation history.
        """
        return self.messages.copy()

    def clear(self):
        """
        Clear the conversation history.
        """
        self.messages.clear()

    def is_empty(self):
        """
        Check whether memory is empty.
        """
        return len(self.messages) == 0