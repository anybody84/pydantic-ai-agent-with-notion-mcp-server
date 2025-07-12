import asyncio

import logfire
from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings

from pydantic_ai_agent.llm.models import open_ai_model
from pydantic_ai_agent.mcp_servers.notion_mcp_server import NotionMCPServerStdio
from pydantic_ai_agent.settings.settings import settings

logfire.configure(send_to_logfire="if-token-present", token=settings.logfire_token, console=False)
logfire.instrument_pydantic_ai()

system_prompt = """
You are a helpful AI kitchen assistant specialized in finding recipes.
Your only source of truth is the "Recipes" page in Notion.
If a recipe is not found, respond with "Recipe not found in Notion".

When you find a recipe, extract the content and present it in the following markdown structure:
- Title: The title of the recipe
- Ingredients: A list of ingredients required for the recipe (exactly as they appear in Notion)
- Instructions: Step-by-step instructions to prepare the recipe (exactly as they appear in Notion)
- Link: A link to the Notion page of the recipe

Don't make up any recipes or provide information not found in Notion. Provide the recipe as is, without any additional commentary.
"""

mcp_server = NotionMCPServerStdio(token=settings.notion_token)
model_settings = ModelSettings(temperature=settings.openai_model_temperature)
recipe_agent = Agent(
    model=open_ai_model, model_settings=model_settings, mcp_servers=[mcp_server], system_prompt=system_prompt
)


def get_user_input(text: str) -> str | None:
    print(text)
    user_input = input("> ").strip()
    return user_input if user_input else None


def should_end_conversation(text: str) -> bool:
    return text.lower() in ["exit", "quit", "stop", "end"]


def logo():
    print("\n========================================")
    print("      Pydantic AI Recipe Agent")
    print("========================================\n")


def instructions():
    print("Welcome to the Pydantic AI Recipe Agent!")
    print("You can ask for recipes and I will retrieve them from Notion.")
    print("Type 'exit', 'quit', 'stop', or 'end' to terminate the conversation.\n")


async def main():
    logfire.info("Starting application")
    logo()
    instructions()
    message_history = []
    user_input = get_user_input("What would you like to cook today?")
    async with recipe_agent.run_mcp_servers():
        while True:
            prompt = f"Provide me with a recipe for {user_input}"
            with logfire.span(f"User: {prompt}"):
                result = await recipe_agent.run(prompt, message_history=message_history)
                message_history.extend(result.new_messages())
                user_input = get_user_input(result.output)
                if should_end_conversation(user_input):
                    print("Ending conversation. Goodbye!")
                    break

        logfire.info("Exiting application")


if __name__ == "__main__":
    asyncio.run(main())
