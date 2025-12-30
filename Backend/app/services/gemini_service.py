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
            "relevance_score": 8,
            "confidence_level": 7,
        }

    def summarize_candidate_profile(self, raw_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Return a concise resume summary and normalized skills list.

        This is currently a stub. Later, replace with a real Gemini call that
        takes the raw_profile fields and generates a rich yet concise summary
        plus a cleaned list of skills.
        """

        # Naive heuristic implementation for now
        name = raw_profile.get("name") or "The candidate"
        target_role = raw_profile.get("target_role") or "the desired role"
        companies = raw_profile.get("companies_worked") or []
        tech_stack = raw_profile.get("tech_stack") or []

        companies_str = ", ".join(companies) if companies else "various organizations"
        tech_str = ", ".join(tech_stack) if tech_stack else "multiple technologies"

        summary = (
            f"{name} is aiming for {target_role}. They have experience at {companies_str} "
            f"and have worked with {tech_str}. This summary is stub-generated and should "
            f"later be replaced by a Gemini-powered description based on the full resume."
        )

        # Combine tech_stack with skills inferred from experiences/projects later
        skills = sorted(set(tech_stack))

        return {"resume_summary": summary, "skills": skills}


gemini_service = GeminiService()
