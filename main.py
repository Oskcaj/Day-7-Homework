import os
import chainlit as cl
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
#import httpx
load_dotenv()

model = OpenAIModel(
    'google/gemini-2.0-flash-lite-001',
    provider=OpenAIProvider(
        base_url='https://openrouter.ai/api/v1',
        api_key=os.getenv("OPENROUTER_API_KEY"),
        #http_client=httpx.AsyncClient(verify=False)
    ),
)

simple_agent = Agent(
    model=model,
    system_prompt=(
        'You are a helpful, humor, emotional bot, please answer everything in traditional chinese.'
    ),   
)

#result_sync = simple_agent.run_sync('What is the capital of Italy?')
#print(result_sync.output)

@cl.on_message
async def on_message(message: cl.Message):
    result = await simple_agent.run(message.content)
    await cl.Message(content=result.output).send()