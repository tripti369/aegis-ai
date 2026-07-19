"""
Configuration settings for the AI Chatbot.

This file contains:
- Model configuration
- Generation parameters
- Conversation memory settings
"""

# ==========================
# LLM Configuration
# ==========================

MODEL_NAME = "llama-3.3-70b-versatile"

# ==========================
# Generation Parameters
# ==========================

DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1000
DEFAULT_TOP_P = 1.0

# ==========================
# Conversation Memory
# ==========================

MAX_HISTORY = 10  # Maximum conversation turns to remember

# ==========================
# Assistant Modes
# ==========================

ASSISTANT_MODES = {
    "General": {
        "temperature": 0.7,
        "max_tokens": 1000,
    },
    "Coding": {
        "temperature": 0.2,
        "max_tokens": 1200,
    },
    "Creative": {
        "temperature": 0.9,
        "max_tokens": 1200,
    },
    "Study": {
        "temperature": 0.5,
        "max_tokens": 1000,
    },
}

DEFAULT_MODE = "General"