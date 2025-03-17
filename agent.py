from __future__ import annotations as _annotations

from dotenv import load_dotenv
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

# Access the API key
openai_api_key = os.getenv('OPENAI_API_KEY')
load_dotenv()

from pydantic_ai import Agent, RunContext
from agent_tools import query_streaming_availability

openai_api_key = os.getenv('OPENAI_API_KEY')

agent = Agent(
    'openai:gpt-4o',
    system_prompt='You are a helpful assistant that provides the streaming availability of movies and TV shows.',
)

@agent.tool
async def check_streaming_availability(ctx: RunContext, title: str) -> str:
    """Check the streaming availability of a movie or TV show.

    Args:
        ctx: The context of the run.
        title: The title of the movie or TV show.
    """
    return await query_streaming_availability(title)