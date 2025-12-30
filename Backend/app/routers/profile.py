from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..db import get_db
from io import BytesIO
from PyPDF2 import PdfReader
from ..services.gemini_service import gemini_service


router = APIRouter()


@router.post("/profile/enrich", response_model=schemas.ProfileEnrichResponse)
def enrich_profile(payload: schemas.CandidateProfileInput, db: Session = Depends(get_db)):
    """Create or update a candidate profile and enrich it via Gemini.

    - Finds or creates a User by email
    - Calls GeminiService.summarize_candidate_profile to get resume_summary + skills
    - Stores resume_summary on User and skills in Skill/UserSkill tables
    """

    # Find or create user by email
    user = db.query(models.User).filter_by(email=payload.email).first()
    if user is None:
        user = models.User(
            name=payload.name,
            email=payload.email,
            role="candidate",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    raw_profile = payload.model_dump()
    enriched = gemini_service.summarize_candidate_profile(raw_profile)
    resume_summary = enriched.get("resume_summary") or ""
    skills = enriched.get("skills") or []

    # Update user resume_summary
    user.resume_summary = resume_summary
    # Persist raw resume text (if provided) for later analysis/debugging
    if payload.resume_text:
        user.resume_raw = payload.resume_text
    db.add(user)
    db.commit()
    db.refresh(user)

    # Persist skills
    normalized_skills = []
    for skill_name in skills:
        normalized = (skill_name or "").strip()
        if not normalized:
            continue

        skill = (
            db.query(models.Skill)
            .filter(models.Skill.skill_name.ilike(normalized))
            .first()
        )
        if skill is None:
            skill = models.Skill(skill_name=normalized)
            db.add(skill)
            db.commit()
            db.refresh(skill)

        link_exists = (
            db.query(models.UserSkill)
            .filter_by(user_id=user.user_id, skill_id=skill.skill_id)
            .first()
        )
        if not link_exists:
            link = models.UserSkill(user_id=user.user_id, skill_id=skill.skill_id)
            db.add(link)
            db.commit()

        normalized_skills.append(skill.skill_name)

    return schemas.ProfileEnrichResponse(
        user_id=user.user_id,
        resume_summary=resume_summary,
        skills=normalized_skills,
    )


@router.post("/profile/upload_resume")
async def upload_resume(file: UploadFile = File(...)) -> dict:
    """Accept a PDF resume upload and return extracted text.

    The frontend can then send this text as `resume_text` to the existing
    `/profile/enrich` endpoint so Gemini can generate a summary & skills.
    """

    if file.content_type not in {"application/pdf", "application/x-pdf"}:
        raise HTTPException(status_code=400, detail="Only PDF resumes are supported")

    content = await file.read()

    # Prefer Gemini's PDF understanding via inlineData; fall back to PyPDF2
    try:
        full_text = gemini_service.extract_resume_text_from_pdf(content)
    except Exception:
        reader = PdfReader(BytesIO(content))
        extracted_text_parts = []
        for page in reader.pages:
            page_text = page.extract_text() or ""
            extracted_text_parts.append(page_text)

        full_text = "\n".join(extracted_text_parts).strip()

    # Truncate to a safe length for downstream LLM calls
    if len(full_text) > 20000:
        full_text = full_text[:20000]

    return {"resume_text": full_text}
