# main.py
from agent.travel_agent import TravelAgent
from livekit.agents import AgentSession, JobContext
from fastapi import FastAPI, Request
from dotenv import load_dotenv
import os
import asyncio

load_dotenv("file.env", override=True)

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Voicebot is running"}

@app.post("/connect")
async def connect(request: Request):
    body = await request.json()
    room = body.get("room")

    if not room:
        return {"error": "Missing 'room' in request body"}

    async def start_agent():
        ctx = JobContext(api_key=os.getenv("LIVEKIT_API_KEY"),
                         api_secret=os.getenv("LIVEKIT_API_SECRET"),
                         ws_url=os.getenv("LIVEKIT_URL"),
                         room=room)
        await ctx.connect()
        session = AgentSession()
        await session.start(agent=TravelAgent(), room=ctx.room)
        await session.say("Hi! I hope you're doing well. Is this a good time to chat about your travel plans?")

    asyncio.create_task(start_agent())
    return {"message": f"Agent started for room {room}"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))  # ✅ Required for Cloud Run
    uvicorn.run("main:app", host="0.0.0.0", port=port)
