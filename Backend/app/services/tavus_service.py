from typing import Any, Dict, Optional

import requests

from ..core_config import get_settings


settings = get_settings()


class TavusService:
    """Wrapper around Tavus CVI Create Conversation API.

    This focuses on creating a real-time conversation and returning
    conversation_id + conversation_url for embedding in the UI.
    """

    BASE_URL = "https://tavusapi.com"

    def __init__(self) -> None:
        self.api_key = settings.TAVUS_API_KEY
        self.persona_id = settings.TAVUS_PERSONA_ID
        self.replica_id = settings.TAVUS_REPLICA_ID

    def _headers(self) -> Dict[str, str]:
        if not self.api_key:
            raise RuntimeError("TAVUS_API_KEY is not configured")
        return {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
        }

    def create_conversation(
        self,
        *,
        persona_id: Optional[str] = None,
        replica_id: Optional[str] = None,
        conversation_name: Optional[str] = None,
        context: Optional[str] = None,
        callback_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Call Tavus Create Conversation endpoint.

        Returns dict with at least conversation_id and conversation_url.
        """

        persona_id = persona_id or self.persona_id
        replica_id = replica_id or self.replica_id
        if not persona_id:
            raise RuntimeError("TAVUS_PERSONA_ID is not configured")

        url = f"{self.BASE_URL}/v2/conversations"
        payload: Dict[str, Any] = {
            "persona_id": persona_id,
        }
        if replica_id:
            payload["replica_id"] = replica_id
        if conversation_name:
            payload["conversation_name"] = conversation_name
        # Some Tavus API configurations do not accept a top-level 'context' field
        # and will return a 400 with "{'context': ['Unknown field.']}". To avoid
        # blocking the flow, we omit it here and rely on persona configuration.
        if callback_url:
            payload["callback_url"] = callback_url

        resp = requests.post(url, headers=self._headers(), json=payload, timeout=60)
        if resp.status_code >= 400:
            raise RuntimeError(f"Tavus error {resp.status_code}: {resp.text}")

        data = resp.json()
        return data

    def send_system_message(self, conversation_id: str, content: str) -> Dict[str, Any]:
        """Send a system message to an existing conversation to provide context.

        This is the Tavus-recommended way to feed interview instructions and
        candidate details. It must be called *after* create_conversation.
        """

        url = f"{self.BASE_URL}/v2/conversations/{conversation_id}/messages"
        payload: Dict[str, Any] = {
            "role": "system",
            "content": content,
        }

        # Tavus docs for messages typically use Bearer auth; we can reuse the
        # same API key but adjust the header format.
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        if resp.status_code >= 400:
            raise RuntimeError(f"Tavus message error {resp.status_code}: {resp.text}")
        return resp.json()


tavus_service = TavusService()
