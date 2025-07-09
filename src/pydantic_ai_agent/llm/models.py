from pydantic_ai.models.openai import OpenAIModel

from pydantic_ai_agent.settings import settings

from .providers import open_ai_provider

open_ai_model = OpenAIModel(settings.openai_model, provider=open_ai_provider)
