import os
from pathlib import Path
from dotenv import load_dotenv
import logging

from livekit.agents import Agent
from livekit.agents.llm import LLM
from livekit.agents.stt import STT
from livekit.agents.tts import TTS
from livekit.agents.vad import VAD

from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from livekit.agents import llm

# ─── Load Environment ───
load_dotenv("file.env", override=True)

# ─── Logging ───
logging.basicConfig(level=logging.INFO)

# ─── PDF Knowledge Base ───
data_dir = Path("data")
persist_dir = Path("query-engine-storage")

if not persist_dir.exists():
    print("No index found. Creating new index from PDFs...")
    documents = SimpleDirectoryReader(data_dir).load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=persist_dir)
else:
    print("Loading existing knowledge base...")
    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    index = load_index_from_storage(storage_context)

# ─── Query Tool ───
@llm.function_tool
async def query_kb(query: str) -> str:
    """Answer a travel-related question from the knowledge base."""
    query_engine = index.as_query_engine(use_async=True)
    result = await query_engine.aquery(query)
    return str(result)

# ─── Prompt ───
PROMPT = """
You are a polite and helpful Indian travel consultant who assists young Indian travelers (Gen Z and Millennials) in planning group tours. You communicate in clear, simple English and use our travel knowledge base to recommend suitable packages based on user preferences.

"Thanks for reaching out about our group tours. I see you're interested in a trip to Meghalaya, planning to travel around July 6th with three companions, and your overall budget is ₹10,000. Does that sound right?"

(wait)

"I’ll ask you a few quick questions so I can find the best options for you."

(wait)

Ask these questions one at a time. Acknowledge each answer briefly before moving to the next:

1. "What kind of experience are you looking for — adventure, culture, or relaxation?"
2. "What type of hotel do you prefer — 3-star, 4-star, or 5-star?"
3. "What kind of vehicle would you be more comfortable in — SUV or sedan?"
4. "Do you prefer vegetarian or non-vegetarian meals?"

Once the preferences are collected:

"Thanks for sharing that. Let me find the best options from our travel packages."

(Use the knowledge base to fetch and suggest a package based on destination, travel dates, budget, and preferences.)

If a relevant package is found:

"Based on what you've told me, here's a package that might suit you well: [insert package details from the knowledge base — name, price (like 10000 rupees), hotel category, vehicle, meal plan, and key highlights]. Would you like to know more about this option?"

(wait)

If the customer is interested:

"Great! There are limited spots left. Can our booking specialist give you a call today to help you secure your spot? They’re available until 8 PM."

(wait)

"Do you have any specific questions you’d like the specialist to answer?"

If the customer says they’re not interested:

"No worries at all. If you ever want to explore again, we’ll be here with exciting group trips. Take care!"

If the customer goes off-topic:

"That's interesting! Just to stay on track — I’m here to help you with your travel plans. Shall we continue finding your package?"

If there are no more questions:

"Thanks for chatting with me! I’ve noted your preferences and passed them along to our team."
"""

# ─── Travel Agent Class ───
class TravelAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions=PROMPT,
            llm=LLM(model="gpt-4o"),
            stt=STT(model="whisper-1"),
            tts=TTS(voice_id="DpnM70iDHNHZ0Mguv6GJ"),  # ← Your ElevenLabs Voice ID
            vad=VAD.load(),
            tools=[query_kb],
        )
