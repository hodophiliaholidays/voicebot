import os
import asyncio
from fastapi import FastAPI
from dotenv import load_dotenv

from livekit.agents import AgentSession
from agent.travel_agent import TravelAgent

load_dotenv("file.env", override=True)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "LiveKit Travel Voicebot is running."}

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_agent())

async def start_agent():
    try:
        session = AgentSession(
            api_key=os.getenv("LIVEKIT_API_KEY"),
            api_secret=os.getenv("LIVEKIT_API_SECRET"),
            ws_url=os.getenv("LIVEKIT_URL")
        )
        await session.start(agent=TravelAgent())
        await session.say("Hi! I hope you're doing well. Is this a good time to chat about your travel plans?")
    except Exception as e:
        print(f"Agent startup error: {e}")
