from openai import OpenAI

from src.config.ai_assistant.settings import (
    OPEN_AI_API_KEY,
    OPEN_AI_BASE_URL,
)
from src.ai_assistant.chat.utils import remove_code_markers
from src.ai_assistant.chat_history import use_cases
client = OpenAI(api_key=OPEN_AI_API_KEY, base_url=OPEN_AI_BASE_URL)

BASE_PROMPT = (
    "User write requests to you, to generate database models,"
    "You generate dbml code for the requests."
    "Output only dbml code."
    "Do not add any other text."
)

async def generate_dbml_code(user_prompt: str) -> str:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": BASE_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        stream=False 
    )

    text_response = response.choices[0].message.content

    return remove_code_markers(text_response)