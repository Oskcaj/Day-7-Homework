import os
from dataclasses import dataclass
from typing import Any
from httpx import AsyncClient

from pydantic_ai import Agent, RunContext, ModelRetry
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

@dataclass
class Deps:
    client: AsyncClient
    weather_api_key: str | None
    geo_api_key: str | None

model = OpenAIModel(
    "google/gemini-2.0-flash-lite-001",
    provider=OpenAIProvider(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )
)

weather_agent = Agent(
    model=model,
    system_prompt=(
        "Be concise, reply with one sentence. "
        "You are a weather assistant and must answer questions using the following two tools:\n"
        "1. `get_lat_lng`: used to query the longitude and latitude of the location entered by the user\n"
        "2. `get_weather`: used to query the real-time weather at the specified longitude and latitude\n"
        "When receiving a query, please use these two tools to process it, and do not guess or respond directly to the result.\n"
        "Only one sentence is allowed to reply to the user after the tool provides the result.\n"
        "Please think and act in English, and keep input in English.\n"
        "After getting the result from the tools, write a friendly and natural sentence to describe the weather condition.\n"
        "Please use the following format to reply to the user:\n"
        "If the user's original question is in Traditional Chinese, translate the final response back into Traditional Chinese."
    ),
    deps_type=Deps,
    retries=2,
    instrument=False,
)

@weather_agent.tool
async def get_lat_lng(ctx: RunContext[Deps], location_description: str) -> dict[str, float]:
    if ctx.deps.geo_api_key is None:
        return {'lat': 51.1, 'lng': -0.1}

    params = {
        'q': location_description,
        'api_key': ctx.deps.geo_api_key,
    }
    r = await ctx.deps.client.get('https://geocode.maps.co/search', params=params)
    r.raise_for_status()
    data = r.json()

    if data:
        return {'lat': float(data[0]['lat']), 'lng': float(data[0]['lon'])}
    else:
        raise ModelRetry('Could not find the location')

@weather_agent.tool
async def get_weather(ctx: RunContext[Deps], lat: float, lng: float) -> dict[str, Any]:
    if ctx.deps.weather_api_key is None:
        return {'temperature': '21°C', 'description': 'Sunny'}

    params = {
        'apikey': ctx.deps.weather_api_key,
        'location': f'{lat},{lng}',
        'units': 'metric',
    }
    r = await ctx.deps.client.get('https://api.tomorrow.io/v4/weather/realtime', params=params)
    r.raise_for_status()
    data = r.json()

    values = data['data']['values']
    code_lookup = {
        1000: 'Clear, Sunny', 1100: 'Mostly Clear', 1101: 'Partly Cloudy', 1102: 'Mostly Cloudy',
        1001: 'Cloudy', 2000: 'Fog', 2100: 'Light Fog', 4000: 'Drizzle',
        4001: 'Rain', 4200: 'Light Rain', 4201: 'Heavy Rain', 5000: 'Snow',
        5001: 'Flurries', 5100: 'Light Snow', 5101: 'Heavy Snow', 6000: 'Freezing Drizzle',
        6001: 'Freezing Rain', 6200: 'Light Freezing Rain', 6201: 'Heavy Freezing Rain',
        7000: 'Ice Pellets', 7101: 'Heavy Ice Pellets', 7102: 'Light Ice Pellets',
        8000: 'Thunderstorm'
    }
    return {
        'temperature': f'{values['temperatureApparent']:0.0f}°C',
        'description': code_lookup.get(values['weatherCode'], 'Unknown'),
    }
