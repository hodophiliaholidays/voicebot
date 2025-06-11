# main.py
from agent.travel_agent import TravelAgent
from livekit.agents import AgentSession, JobContext, WorkerOptions
from livekit.agents.cli import run_worker  # CLI version

import os
from dotenv import load_dotenv

load_dotenv("file.env", override=True)

async def entrypoint(ctx: JobContext):
    await ctx.connect()
    session = AgentSession()
    await session.start(agent=TravelAgent(), room=ctx.room)
    await session.say("Hi! I hope you're doing well. Is this a good time to chat about your travel plans?")

def start():
    run_worker(
        entrypoint_fnc=entrypoint,
        api_key=os.getenv("LIVEKIT_API_KEY"),
        api_secret=os.getenv("LIVEKIT_API_SECRET"),
        ws_url=os.getenv("LIVEKIT_URL"),
    )

if __name__ == "__main__":
    start()
