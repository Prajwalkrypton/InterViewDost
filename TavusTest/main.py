import os
import json
from typing import Optional

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


load_dotenv()

app = FastAPI(title="Tavus Avatar Demo API")

# Simple CORS so you can open the HTML file directly or from another dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    text: Optional[str] = None


class GenerateResponse(BaseModel):
    conversation_url: Optional[str]
    raw_response: dict


@app.post("/generate", response_model=GenerateResponse)
async def generate_avatar_video(body: GenerateRequest):
    api_key = os.getenv("TAVUS_API_KEY")
    persona_id = os.getenv("TAVUS_PERSONA_ID")
    replica_id = os.getenv("TAVUS_REPLICA_ID")

    if not api_key or not persona_id:
        raise HTTPException(
            status_code=500,
            detail="TAVUS_API_KEY or TAVUS_PERSONA_ID not configured on server",
        )

    script_text = body.text or (
        "In this demo, we are testing a realistic AI avatar for interview simulations. "
        "The goal is to check whether the lip movements are synchronized with the spoken words. "
        "If this works correctly, we will integrate this avatar into a full AI-powered interview system."
    )

    # Tavus Create Conversation endpoint (per docs)
    # See: https://docs.tavus.io/api-reference/conversations/create-conversation
    url = "https://tavusapi.com/v2/conversations"

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }

    payload: dict = {
        "persona_id": persona_id,
        # Optional friendly name for debugging in Tavus dashboard
        "conversation_name": "InterviewDost TavusTest Conversation",
    }

    # replica_id is optional if persona has a default replica; include if provided
    if replica_id:
        payload["replica_id"] = replica_id

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=f"Error calling Tavus: {e}") from e

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    try:
        data = resp.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=502, detail="Tavus returned non-JSON response")

    # Extract conversation_url from Tavus response
    conversation_url: Optional[str] = None
    if isinstance(data, dict) and isinstance(data.get("conversation_url"), str):
        conversation_url = data["conversation_url"]

    return GenerateResponse(conversation_url=conversation_url, raw_response=data)


@app.get("/")
async def root():
    return {"message": "Tavus Avatar Demo API running. POST /generate with {text}."}
