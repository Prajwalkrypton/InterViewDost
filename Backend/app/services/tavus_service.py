from typing import Any, Dict, Optional, Tuple

import logging

import requests
from requests import RequestException

from ..core_config import get_settings


settings = get_settings()

logger = logging.getLogger(__name__)


class TavusService:
    """Wrapper around Tavus CVI Create Conversation API.

    This focuses on creating a real-time conversation and returning
    conversation_id + conversation_url for embedding in the UI.
    """

    # Use the Tavus CVI base URL that is reachable from this environment.
    # The older host "tavusapi.com" is currently responding correctly for
    # conversation creation and returns `conversation_url`.
    BASE_URL = "https://tavusapi.com"

    def __init__(self) -> None:
        logger.info("TavusService: initializing (no API call)")
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

    def _extract_conversation_fields(self, data: Any) -> Tuple[Optional[str], Optional[str]]:
        if not isinstance(data, dict):
            return None, None

        conv_id = data.get("conversation_id") or data.get("id")
        conv_url = data.get("conversation_url") or data.get("conversationUrl")
        if conv_id or conv_url:
            return conv_id, conv_url

        nested = data.get("data")
        if isinstance(nested, dict):
            conv_id = nested.get("conversation_id") or nested.get("id")
            conv_url = nested.get("conversation_url") or nested.get("conversationUrl")
            return conv_id, conv_url

        return None, None

    def get_conversation(self, conversation_id: str) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/v2/conversations/{conversation_id}"
        try:
            resp = requests.get(url, headers=self._headers(), timeout=20)
        except RequestException as exc:
            raise RuntimeError(f"Tavus network error: {exc}") from exc

        if resp.status_code >= 400:
            raise RuntimeError(f"Tavus error {resp.status_code}: {resp.text}")

        return resp.json()

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
        logger.info("TavusService.create_conversation: calling Tavus API (this consumes credits)")

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
        if context:
            payload["conversational_context"] = context
        if callback_url:
            payload["callback_url"] = callback_url

        last_exc: Exception | None = None
        for attempt in range(2):
            try:
                resp = requests.post(url, headers=self._headers(), json=payload, timeout=25)
                if resp.status_code >= 400:
                    raise RuntimeError(f"Tavus error {resp.status_code}: {resp.text}")

                data = resp.json()
                conv_id, conv_url = self._extract_conversation_fields(data)
                if conv_id and not conv_url:
                    try:
                        detail = self.get_conversation(conv_id)
                        _, conv_url = self._extract_conversation_fields(detail)
                        if conv_url:
                            data["conversation_url"] = conv_url
                    except RuntimeError as e:
                        logger.warning("Tavus conversation created but url lookup failed: %s", e)

                return data
            except (RequestException, RuntimeError) as exc:
                last_exc = exc
                if attempt == 0:
                    continue
                raise RuntimeError(f"Tavus network error: {exc}") from exc

        raise RuntimeError(f"Tavus network error: {last_exc}")

    def send_system_message(self, conversation_id: str, content: str) -> Dict[str, Any]:
        """Send a system message to an existing conversation to provide context.

        This is the Tavus-recommended way to feed interview instructions and
        candidate details. It must be called *after* create_conversation.
        """
        logger.info("TavusService.send_system_message: calling Tavus API (this consumes credits)")

        url = f"{self.BASE_URL}/v2/conversations/{conversation_id}/messages"
        payload: Dict[str, Any] = {
            "role": "system",
            "content": content,
        }

        headers_to_try = [
            {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            self._headers(),
        ]

        last_error: str | None = None
        for headers in headers_to_try:
            try:
                resp = requests.post(url, headers=headers, json=payload, timeout=25)
            except RequestException as exc:
                last_error = str(exc)
                continue

            if resp.status_code < 400:
                return resp.json()

            last_error = f"{resp.status_code}: {resp.text}"

        raise RuntimeError(f"Tavus message error {last_error}")


tavus_service = TavusService()
