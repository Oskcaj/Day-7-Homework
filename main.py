from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
# change to use pydantic AI
#from openai import AsyncOpenAI
import os
#import chainlit as cl

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
        'You are a helpful, humor, emotional bot, you always reply in Traditional Chinese'
    ),   
)

result_sync = simple_agent.run_sync('What is the capital of Italy?')
print(result_sync.output)

# client = AsyncOpenAI()
#client = AsyncOpenAI(
    #base_url="https://openrouter.ai/api/v1",
    #api_key=os.getenv("OPENROUTER_API_KEY"),
    #http_client = httpx.AsyncClient(verify=False)
#)

# Instrument the OpenAI client
#cl.instrument_openai()

#settings = {
   # "model": "google/gemini-2.0-flash-lite-001",
   # "temperature": 0,
    # ... more settings
#}

#@cl.on_message
#async def on_message(message: cl.Message):
    #response = await client.chat.completions.create(
       # messages=[
         #   {
         #       "content": "You are a helpful, humor, emotional bot, you always reply in Traditional Chinese",
          #      "role": "system"
         #   },
          #  {
          #      "content": message.content,
          #      "role": "user"
#            }
        #],
      #  **settings
  #  )
   # await cl.Message(content=response.choices[0].message.content).send()