from openai import OpenAI
from config import GROQ_API_KEY
from prompts import SYSTEM_PROMPT

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def get_ai_response(user_message: str) -> str:
    """
    Sends the user's message to the Groq LLM
    and returns the generated response.
    """

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages = [
               {
                    "role": "system",
                    "content": SYSTEM_PROMPT
               },
               {
                    "role": "user",
                    "content": user_message
               }
       ]

        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Error: {str(e)}"