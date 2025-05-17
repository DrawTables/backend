from openai import OpenAI

from src.ai_assistant.chat.utils import remove_code_markers
from src.config.ai_assistant.settings import OPEN_AI_API_KEY, OPEN_AI_BASE_URL

client = OpenAI(api_key=OPEN_AI_API_KEY, base_url=OPEN_AI_BASE_URL)

DBML_BASE_PROMPT = (
    "User write requests to you, to generate database models."
    "You generate dbml code for the requests."
    "You must use user context to rewrite or generate new schemas if it designated"
    "User context: {}"
    "Output only dbml code."
    "Do not add any other text."
)

SQL_BASE_PROMPT = (
    "User write requests to you, to generate database queries."
    "You generate sql code for the requests."
    "You must use user context with dbml schemas to generate new queries if it designated"
    "User context: {}"
    "Output only sql code."
    "Do not add any other text."
)

async def generate_dbml_code(user_prompt: str, user_context: str | None) -> str:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": DBML_BASE_PROMPT.format(user_context if user_context else "")},
            {"role": "user", "content": user_prompt},
        ],
        stream=False,
    )

    text_response = response.choices[0].message.content

    return remove_code_markers(text_response)


async def generate_sql_code(user_prompt: str, user_context: str | None) -> str:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": SQL_BASE_PROMPT.format(user_context if user_context else "")},
            {"role": "user", "content": user_prompt},
        ],
        stream=False,
    )
    text_response = response.choices[0].message.content
    return remove_code_markers(text_response)