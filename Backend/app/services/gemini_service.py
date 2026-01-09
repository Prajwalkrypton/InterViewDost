from typing import Any, Dict, List

import requests

from ..core_config import get_settings


settings = get_settings()


class GeminiService:
    """Wrapper around Gemini API for question generation and answer evaluation."""

    def __init__(self) -> None:
        self.api_key = settings.GEMINI_API_KEY
        # You can change the model name here if needed.
        self.model = "gemini-1.5-flash"
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

    def _generate(self, prompt: str, system_instruction: str | None = None) -> str:
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")

        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"

        contents: List[Dict[str, Any]] = []
        if system_instruction:
            contents.append({"role": "user", "parts": [{"text": system_instruction}]})
        contents.append({"role": "user", "parts": [{"text": prompt}]})

        payload = {"contents": contents}

        resp = requests.post(url, json=payload, timeout=60)
        if resp.status_code >= 400:
            raise RuntimeError(f"Gemini error {resp.status_code}: {resp.text}")

        data = resp.json()
        candidates = data.get("candidates") or []
        if not candidates:
            return ""

        parts = (candidates[0].get("content") or {}).get("parts") or []
        texts = [p.get("text", "") for p in parts]
        return " ".join(texts).strip()

    def extract_resume_text_from_pdf(self, pdf_bytes: bytes) -> str:
        """Use Gemini to extract plain text from a PDF resume.

        This sends the PDF as inlineData and asks Gemini to return only the
        extracted plain text. This generally yields better structure than
        basic PDF parsing.
        """

        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")

        import base64

        b64 = base64.b64encode(pdf_bytes).decode("utf-8")

        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"

        contents: List[Dict[str, Any]] = [
            {
                "role": "user",
                "parts": [
                    {
                        "inlineData": {
                            "mimeType": "application/pdf",
                            "data": b64,
                        }
                    },
                    {
                        "text": (
                            "Extract and return the full plain-text content of this resume. "
                            "Return only plain text, no markdown or JSON."
                        )
                    },
                ],
            }
        ]

        resp = requests.post(url, json={"contents": contents}, timeout=90)
        if resp.status_code >= 400:
            raise RuntimeError(f"Gemini PDF error {resp.status_code}: {resp.text}")

        data = resp.json()
        candidates = data.get("candidates") or []
        if not candidates:
            return ""
        parts = (candidates[0].get("content") or {}).get("parts") or []
        texts = [p.get("text", "") for p in parts]
        return " ".join(texts).strip()

    def generate_question(self, candidate_profile: Dict[str, Any]) -> str:
        role = candidate_profile.get("role") or "this role"
        name = candidate_profile.get("name") or "the candidate"
        summary = candidate_profile.get("resume_summary") or ""
        skills = candidate_profile.get("skills") or []
        skills_str = ", ".join(skills) if skills else "unspecified skills"

        prompt = (
            f"You are an AI interviewer preparing the very first question for a mock "
            f"interview. The candidate is {name}, targeting the role '{role}'. "
            f"Their summarized background is: {summary}\n"
            f"Key skills: {skills_str}.\n\n"
            "Write a single, open-ended first question that invites them to introduce "
            "themselves and connect their experience to this role. Return only the question text."
        )

        try:
            text = self._generate(prompt)
            return text or "To start, could you briefly introduce yourself and explain why you are a good fit for this role?"
        except RuntimeError:
            return "To start, could you briefly introduce yourself and explain why you are a good fit for this role?"

    def evaluate_answer(self, question: str, answer: str) -> Dict[str, int]:
        prompt = (
            "You are evaluating a candidate's answer in a mock interview. "
            "Given the question and answer, provide two integer scores from 1 to 10: "
            "relevance_score and confidence_level. Respond strictly as JSON, for example: "
            "{\"relevance_score\": 8, \"confidence_level\": 7}.\n\n"
            f"Question: {question}\n\nAnswer: {answer}"
        )

        try:
            raw = self._generate(prompt)
            import json

            data = json.loads(raw)
            rel = int(data.get("relevance_score", 7))
            conf = int(data.get("confidence_level", 7))
            rel = max(1, min(10, rel))
            conf = max(1, min(10, conf))
            return {"relevance_score": rel, "confidence_level": conf}
        except Exception:
            return {"relevance_score": 8, "confidence_level": 7}

    def summarize_candidate_profile(self, raw_profile: Dict[str, Any]) -> Dict[str, Any]:
        name = raw_profile.get("name") or "The candidate"
        target_role = raw_profile.get("target_role") or "the desired role"
        companies = raw_profile.get("companies_worked") or []
        tech_stack = raw_profile.get("tech_stack") or []
        resume_text = raw_profile.get("resume_text") or ""

        companies_str = "; ".join(companies)
        tech_str = ", ".join(tech_stack)

        system_instruction = (
            "You are helping summarize a candidate's background for an AI interviewer. "
            "Given structured profile fields and optional raw resume text, write a concise "
            "2-4 sentence resume-style summary and extract a cleaned list of 5-15 key skills."
        )

        prompt = (
            f"Name: {name}\n"
            f"Target role: {target_role}\n"
            f"Companies worked: {companies_str or 'N/A'}\n"
            f"Tech stack: {tech_str or 'N/A'}\n\n"
        )
        if resume_text:
            prompt += f"Resume text:\n{resume_text}\n\n"

        prompt += (
            "Return your answer strictly as JSON with two fields: "
            "`resume_summary` (string) and `skills` (array of strings)."
        )

        try:
            raw = self._generate(prompt, system_instruction)
            import json

            data = json.loads(raw)
            summary = str(data.get("resume_summary") or "")
            skills = data.get("skills") or []
            skills = [str(s).strip() for s in skills if str(s).strip()]
            return {"resume_summary": summary, "skills": skills}
        except Exception:
            # Fallback: simple heuristic if Gemini fails
            base_summary = (
                f"{name} is aiming for {target_role}. They have worked at {companies_str or 'various organizations'} "
                f"and used technologies such as {tech_str or 'multiple technologies'}."
            )
            return {"resume_summary": base_summary, "skills": tech_stack}

    def summarize_interview(self, interview: Dict[str, Any], qa_items: list[Dict[str, Any]]) -> Dict[str, str]:
        candidate_name = interview.get("candidate_name") or "The candidate"
        role = interview.get("role") or "the target role"

        qa_text_lines = []
        for idx, item in enumerate(qa_items, start=1):
            q = item.get("question") or ""
            a = item.get("answer") or "(no answer recorded)"
            qa_text_lines.append(f"Q{idx}: {q}\nA{idx}: {a}")

        qa_block = "\n\n".join(qa_text_lines)

        system_instruction = (
            "You are an interview coach generating feedback after a mock interview. "
            "Given the role and a list of questions and answers, write: (1) a concise "
            "overall comments paragraph, and (2) a suggestions paragraph with concrete "
            "next steps."
        )

        prompt = (
            f"Candidate name: {candidate_name}\n"
            f"Target role: {role}\n\n"
            f"Transcript (questions and answers):\n{qa_block}\n\n"
            "Return strictly as JSON: {\"comments\": string, \"suggestions\": string}."
        )

        try:
            raw = self._generate(prompt, system_instruction)
            import json

            data = json.loads(raw)
            comments = str(data.get("comments") or "")
            suggestions = str(data.get("suggestions") or "")
            return {"comments": comments, "suggestions": suggestions}
        except Exception:
            fallback_comments = (
                f"{candidate_name} completed a mock interview for {role}. This is fallback feedback "
                "used when the Gemini API response could not be parsed."
            )
            fallback_suggestions = (
                "Focus on giving structured, specific examples (STAR format) and highlight measurable impact."
            )
            return {"comments": fallback_comments, "suggestions": fallback_suggestions}

    def generate_tavus_interviewer_context(self, payload: Dict[str, Any]) -> str:
        """Generate compact Tavus conversation context from stored profile + resume.

        Tavus CVI supports a `context` field at conversation creation which gets
        appended to the persona/system prompt. We keep this concise to improve
        avatar grounding without hitting context limits.
        """

        name = payload.get("name") or "Candidate"
        target_role = payload.get("target_role") or payload.get("interview_type") or "the role"
        skills = payload.get("skills") or []
        resume_summary = payload.get("resume_summary") or ""
        resume_raw = payload.get("resume_raw") or ""

        if isinstance(skills, list):
            skills_str = ", ".join([str(s).strip() for s in skills if str(s).strip()])
        else:
            skills_str = str(skills)

        if resume_raw and len(resume_raw) > 12000:
            resume_raw = resume_raw[:12000]

        system_instruction = (
            "You are preparing context for an AI interviewer avatar. "
            "Write a clear, compact conversational_context that will be appended to a system prompt. "
            "It must tell the interviewer who the candidate is, what role they target, their key skills, "
            "and 5-8 high-signal facts from the resume. Also include strict interviewing guidelines. "
            "Return ONLY plain text (no markdown, no JSON). Keep it under 1800 characters."
        )

        prompt = (
            f"Candidate name: {name}\n"
            f"Target role: {target_role}\n"
            f"Skills: {skills_str or 'N/A'}\n\n"
        )
        if resume_summary:
            prompt += f"Resume summary:\n{resume_summary}\n\n"
        if resume_raw:
            prompt += f"Resume raw text (may be noisy):\n{resume_raw}\n\n"

        prompt += (
            "Now produce the interviewer context. Include:\n"
            "- a short candidate briefing\n"
            "- what to probe (projects, skills, gaps)\n"
            "- interview structure (intro, technical, behavioral, closing)\n"
            "- tone and constraints (professional, friendly, ask one question at a time)"
        )

        try:
            ctx = self._generate(prompt, system_instruction)
            ctx = (ctx or "").strip()
            if len(ctx) > 1800:
                ctx = ctx[:1800]
            return ctx
        except Exception:
            fallback = (
                "You are an AI interviewer. Interview the candidate for "
                f"{target_role}. Candidate: {name}. "
                f"Skills: {skills_str or 'N/A'}. "
                f"Resume summary: {resume_summary or 'N/A'}. "
                "Guidelines: Be professional and friendly. Ask one question at a time. "
                "Start with a brief intro, then ask about background, projects, and key skills. "
                "Include behavioral questions (STAR), then close with next steps."
            )
            return fallback[:1800]


gemini_service = GeminiService()
