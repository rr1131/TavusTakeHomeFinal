from __future__ import annotations
import os
import json
from typing import List, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from tavus import Tavus

# load environment vars from .env
load_dotenv()

app = FastAPI(title="Tavus Customer Advocate Takehome")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# environment variable reader
def _env(name: str, default: Optional[str] = None) -> str:
    v = os.getenv(name, default)
    return "" if v is None else v

# to parse the DOCUMENT_IDs
def _parse_csv(csv: str) -> List[str]:
    return [x.strip() for x in csv.split(",") if x.strip()]

# get needed Tavus Config from .env
TAVUS_API_KEY = _env("TAVUS_API_KEY")
PERSONA_ID = _env("PERSONA_ID")
REPLICA_ID = _env("REPLICA_ID")
DOCUMENT_IDS = _parse_csv(_env("DOCUMENT_IDS", ""))
REQUIRE_AUTH = _env("REQUIRE_AUTH", "false").lower() == "true"

# API client wrapper
client = Tavus(TAVUS_API_KEY)

# for demoing with index.html
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "persona_id": PERSONA_ID,
            "replica_id": REPLICA_ID,
            "document_ids": DOCUMENT_IDS,
            "require_auth": REQUIRE_AUTH,
        },
    )

# Create new CVI conversation
@app.post("/start")
def start_session():

    # Both of these are required
    if not PERSONA_ID:
        raise HTTPException(status_code=500, detail="Missing PERSONA_ID in env")
    if not REPLICA_ID:
        raise HTTPException(status_code=500, detail="Missing REPLICA_ID in env")

    conversation_name = "Public Speaking Coach meets with Rod"
    custom_greeting = "Hey Rod! I'm Chuck, a public speaking coach. What are you practicing today, and what kind of feedback would help most?"

    conversational_context = (
        "Run a structured two-take coaching session. "
        "First, ask what the user is practicing and what feedback they want. "
        "Then the user delivers a short intro; do not interrupt. "
        "Give one round of feedback (max 2 notes: one visual, one vocal) with no labels. "
        "Then the user retries; do not interrupt. "
        "After the retry, highlight what improved and end with encouragement. "
        "Do not ask for additional takes."
    )

    payload_preview = {
        "persona_id": PERSONA_ID,
        "replica_id": REPLICA_ID,
        "conversation_name": conversation_name,
        "custom_greeting": custom_greeting,
        "conversational_context": conversational_context,
        "document_ids": DOCUMENT_IDS or None,
        "document_retrieval_strategy": "balanced",
        "require_auth": REQUIRE_AUTH,
        "max_participants": 2,
    }
    print("\n--- Payload preview (app layer) ---")
    print(json.dumps(payload_preview, indent=2))
    print("-----------------------------------\n")

    try:
        # API call to create conversation from environment vars
        # and locally defined conversation_name, custom_greeting 
        # and conversational context
        result = client.create_conversation(
            persona_id=PERSONA_ID,
            replica_id=REPLICA_ID,
            conversation_name=conversation_name,
            conversational_context=conversational_context,
            custom_greeting=custom_greeting,
            document_ids=DOCUMENT_IDS or None,
            document_retrieval_strategy="balanced",
            require_auth=REQUIRE_AUTH,
            max_participants=2,
        )

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

    return {
        "conversation_id": result.conversation_id,
        "conversation_url": result.conversation_url,
        "status": result.status,
    }

