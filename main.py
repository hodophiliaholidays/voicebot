import os
import asyncio
from fastapi import FastAPI
from dotenv import load_dotenv

from livekit.agents import AgentSession
from agent.travel_agent import TravelAgent

# Load environment variables
load_dotenv("file.env", override=True)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "LiveKit Travel Voicebot is running."}

@app.on_event("startup")
async def startup_event():
    print("🚀 FastAPI app started. Launching background services...")
    # Don't block the server — run agent/index startup in background
    asyncio.create_task(initialize_everything())

async def initialize_everything():
    try:
        print("🧠 Initializing LlamaIndex and LiveKit agent...")
        
        # --- LiveKit Agent Session ---
        session = AgentSession(
            api_key=os.getenv("LIVEKIT_API_KEY"),
            api_secret=os.getenv("LIVEKIT_API_SECRET"),
            ws_url=os.getenv("LIVEKIT_URL")
        )
        
        # Start the travel assistant
        await session.start(agent=TravelAgent())
        print("✅ Travel agent started.")

        # Speak welcome message (don't block, run in background)
        asyncio.create_task(session.say("Hi! I hope you're doing well. Is this a good time to chat about your travel plans?"))
        print("💬 Initial message queued.")
        
    except Exception as e:
        print(f"❌ Agent startup error: {e}")
