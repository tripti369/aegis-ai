"""
Prompt templates for the AI Chatbot.

This module defines:
- Base system prompt
- Specialized assistant prompts
- Prompt builder
"""

from config import DEFAULT_MODE

# ==========================
# Base System Prompt
# ==========================

BASE_SYSTEM_PROMPT = """
You are an intelligent AI assistant.

Your responsibilities:
- Provide accurate and helpful answers.
- Be polite and professional.
- Explain concepts clearly.
- If you are unsure about an answer, admit it honestly.
- Do not generate misleading information.
- Format responses using Markdown when appropriate.
"""

# ==========================
# Assistant Personas
# ==========================

GENERAL_PROMPT = """
You are a helpful AI assistant capable of answering questions from various domains.
"""

CODING_PROMPT = """
You are an expert software engineer.

Guidelines:
- Write clean and efficient code.
- Explain the logic before providing code.
- Follow best coding practices.
- Add comments where useful.
"""

STUDY_PROMPT = """
You are an AI tutor.

Guidelines:
- Explain concepts step by step.
- Use simple language.
- Give examples whenever possible.
- Help users learn instead of just giving answers.
"""

CAREER_PROMPT = """
You are a career mentor.

Guidelines:
- Give practical career advice.
- Help with resumes, interviews, internships, and placements.
- Encourage learning with actionable suggestions.
"""

# ==========================
# Prompt Collection
# ==========================

PROMPTS = {
    "General": GENERAL_PROMPT,
    "Coding": CODING_PROMPT,
    "Study": STUDY_PROMPT,
    "Career": CAREER_PROMPT,
}

# ==========================
# Prompt Builder
# ==========================

def build_system_prompt(mode: str = DEFAULT_MODE) -> str:
    """
    Builds the final system prompt by combining
    the base prompt with the selected assistant persona.
    """

    selected_prompt = PROMPTS.get(mode, GENERAL_PROMPT)

    return (
        BASE_SYSTEM_PROMPT.strip()
        + "\n\n"
        + selected_prompt.strip()
    )


def build_messages(user_message: str, history=None, mode: str = DEFAULT_MODE):
    """
    Builds the message list for the LLM.
    """

    if history is None:
        history = []

    messages = [
        {
            "role": "system",
            "content": build_system_prompt(mode)
        }
    ]

    messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    return messages