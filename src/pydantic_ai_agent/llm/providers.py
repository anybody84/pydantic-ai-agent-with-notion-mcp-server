from pydantic_ai.providers.openai import OpenAIProvider

from pydantic_ai_agent.settings.settings import settings

open_ai_provider = OpenAIProvider(
    api_key=settings.openai_api_key,
)
