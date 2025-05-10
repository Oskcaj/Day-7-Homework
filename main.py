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
    try:
        result = await simple_agent.run(message.content)
        output = result.output if result and result.output else "⚠️ 沒有收到模型回應"
    except Exception as e:
        output = f"❌ 發生錯誤：{str(e)}"
    await cl.Message(content=output).send()
    
if not os.getenv("OPENROUTER_API_KEY"):
    raise RuntimeError("❌ 環境變數 OPENROUTER_API_KEY 未設定，請檢查 .env 或 Cloud Run 設定")