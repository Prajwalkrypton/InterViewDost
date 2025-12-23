from typing import Any, Dict

from ..core_config import get_settings


settings = get_settings()


class GeminiService:
    """Wrapper around Gemini API for question generation and answer evaluation.

    For now, this is a stub that you can later expand to real HTTP calls to the
    Gemini API using `settings.GEMINI_API_KEY`.
    """

    def __init__(self) -> None:
        self.api_key = settings.GEMINI_API_KEY

    def generate_question(self, candidate_profile: Dict[str, Any]) -> str:
        """Generate the next interview question.

        Currently a simple deterministic template; replace with real Gemini call.
        """

        role = candidate_profile.get("role")
        base = "Tell me about yourself and how your background fits this role."
        if role:
            return (
                "To start, could you briefly introduce yourself and explain why you "
                f"are a good fit for the {role} role?"
            )
        return base

    def evaluate_answer(self, question: str, answer: str) -> Dict[str, int]:
        """Evaluate an answer and return simple scores.

        This stub uses only length-based heuristics. Replace with Gemini.
        """

        length = len(answer.split())
        if length < 5:
            score = 1
        elif length < 20:
            score = 3
        else:
            score = 5

        return {
            "relevance_score": score,
            "confidence_level": score,
        }


gemini_service = GeminiService()
