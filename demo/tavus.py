from __future__ import annotations
import json
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import requests


TAVUS_URL = "https://tavusapi.com/v2"

class TavusError(RuntimeError):
    pass

@dataclass
class CreateConversationResult:
    conversation_id: str
    conversation_url: str
    status: str
    meeting_token: Optional[str] = None

# Lightweight Tavus API client
class Tavus:
    
    # constructor
    def __init__(self, api_key: str, url: str = TAVUS_URL) -> None:
        if not api_key:
            raise ValueError("Missing Tavus API key. Cannot proceed.")
        self.api_key = api_key
        self.url = url.rstrip("/")

        # logging setup
        self.logger = logging.getLogger("tavus")
        if not self.logger.handlers:
            logging.basicConfig(level=logging.INFO)
    
    # generate required HTTP headers
    def _headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
        }

    # create conversation session
    def create_conversation(
        self,
        *,
        persona_id: str,
        replica_id: str,
        conversation_name: Optional[str] = None,
        conversational_context: Optional[str] = None,
        custom_greeting: Optional[str] = None,
        document_ids: Optional[List[str]] = None,
        document_retrieval_strategy: Optional[str] = None,  # speed|balanced|quality
        require_auth: bool = False,
        max_participants: int = 2,
        test_mode: bool = False,
        audio_only: bool = False,
        callback_url: Optional[str] = None,
        memory_stores: Optional[List[str]] = None,
        properties: Optional[Dict[str, Any]] = None,
    ) -> CreateConversationResult:
        if not persona_id or not replica_id:
            raise ValueError("persona_id and replica_id are required for conversation")

        payload: Dict[str, Any] = {
            "persona_id": persona_id,
            "replica_id": replica_id,
            "require_auth": bool(require_auth),
            "max_participants": max(2, int(max_participants)),
            "test_mode": bool(test_mode),
            "audio_only": bool(audio_only),
        }

        if conversation_name:
            payload["conversation_name"] = conversation_name
        if conversational_context:
            payload["conversational_context"] = conversational_context
        if custom_greeting:
            payload["custom_greeting"] = custom_greeting
        if callback_url:
            payload["callback_url"] = callback_url
        if memory_stores:
            payload["memory_stores"] = memory_stores
        if document_ids:
            payload["document_ids"] = document_ids
        if document_retrieval_strategy:
            payload["document_retrieval_strategy"] = document_retrieval_strategy
        if properties:
            payload["properties"] = properties

        self.logger.info("Create Conversation payload:\n%s", json.dumps(payload, indent=2))
        self.logger.info("Using persona: %s | KB docs: %s", persona_id, document_ids)

        post_url = f"{self.url}/conversations"
        resp = requests.post(post_url, headers=self._headers(), json=payload, timeout=30)

        if resp.status_code >= 400:
            raise TavusError(f"Tavus API error {resp.status_code}: {resp.text}")

        data = resp.json()
        return CreateConversationResult(
            conversation_id=data["conversation_id"],
            conversation_url=data["conversation_url"],
            status=data.get("status", "unknown"),
            meeting_token=data.get("meeting_token"),
        )
