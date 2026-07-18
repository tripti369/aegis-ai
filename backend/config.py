import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Read Groq API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Check if key exists
if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. Please add it to your .env file."
    )