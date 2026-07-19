"""
LLM Interface

Backend Lead will replace this function
with the actual Groq API implementation.
"""


"""
LLM Interface

This module is responsible for communicating
with the Groq API.

Backend Lead: Harshita
"""

from openai import OpenAI

from config import (
    GROQ_API_KEY,
    MODEL_NAME,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS,
    DEFAULT_TOP_P,
)

# Create Groq Client
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


def generate_response(messages, model_config=None):
    """
    Sends the conversation to the Groq LLM
    and returns the generated response.
    """

    try:

        # Use default settings
        temperature = DEFAULT_TEMPERATURE
        max_tokens = DEFAULT_MAX_TOKENS
        top_p = DEFAULT_TOP_P

        # Override if a specific mode provides values
        if model_config:
            temperature = model_config.get(
                "temperature",
                DEFAULT_TEMPERATURE
            )

            max_tokens = model_config.get(
                "max_tokens",
                DEFAULT_MAX_TOKENS
            )

            top_p = model_config.get(
                "top_p",
                DEFAULT_TOP_P
            )

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"