import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..db import get_db
from ..services.gemini_service import gemini_service
from ..services.tavus_service import tavus_service

router = APIRouter()

logger = logging.getLogger(__name__)


# --- Routes -------------------------------------------------------------------


@router.post("/start", response_model=schemas.InterviewStartResponse)
def start_interview(payload: schemas.InterviewStartRequest, db: Session = Depends(get_db)):
    # Create or reuse candidate user.
    # If a user with this email already exists (e.g. the seeded admin), reuse
    # that row instead of inserting a new one to avoid unique email conflicts.
    cand_data = payload.candidate

    candidate = None
    if cand_data.email:
        candidate = db.query(models.User).filter_by(email=cand_data.email).first()

    if candidate is None:
        candidate = models.User(
            name=cand_data.name,
            email=cand_data.email,
            password_hash=cand_data.password_hash,
            role=cand_data.role or "candidate",
            resume_summary=cand_data.resume_summary,
        )
        db.add(candidate)
        db.commit()
        db.refresh(candidate)

    # Attach skills to candidate if provided
    skill_names: list[str] = []
    if payload.skills:
        for skill_name in payload.skills:
            normalized = (skill_name or "").strip()
            if not normalized:
                continue
            existing_skill = (
                db.query(models.Skill)
                .filter(models.Skill.skill_name.ilike(normalized))
                .first()
            )
            if existing_skill is None:
                existing_skill = models.Skill(skill_name=normalized)
                db.add(existing_skill)
                db.commit()
                db.refresh(existing_skill)

            link_exists = (
                db.query(models.UserSkill)
                .filter_by(user_id=candidate.user_id, skill_id=existing_skill.skill_id)
                .first()
            )
            if not link_exists:
                user_skill = models.UserSkill(
                    user_id=candidate.user_id,
                    skill_id=existing_skill.skill_id,
                    proficiency=None,
                )
                db.add(user_skill)
                db.commit()

            skill_names.append(existing_skill.skill_name)

    # For now, interviewer is not created dynamically; we require an interviewer_id
    if payload.interviewer_id is None:
        raise HTTPException(status_code=400, detail="interviewer_id is required")

    interviewer = db.query(models.User).filter_by(user_id=payload.interviewer_id).first()
    if not interviewer:
        raise HTTPException(status_code=404, detail="Interviewer not found")

    interview = models.Interview(
        candidate_id=candidate.user_id,
        interviewer_id=interviewer.user_id,
        date=payload.date,
        time=payload.time,
        type=payload.interview_type,
    )
    db.add(interview)
    db.commit()
    db.refresh(interview)

    # Create Tavus CVI conversation for this interview
    candidate_profile = {
        "name": candidate.name,
        "email": candidate.email,
        "role": candidate.role,
        "resume_summary": candidate.resume_summary,
        "resume_raw": candidate.resume_raw,
        "skills": skill_names,
    }

    skills_section = ", ".join(skill_names) if skill_names else "(skills not provided)"
    resume_section = candidate.resume_summary or "No explicit resume summary was provided."

    context_str = gemini_service.generate_tavus_interviewer_context(
        {
            "name": candidate_profile.get("name"),
            "target_role": candidate_profile.get("role") or payload.interview_type,
            "interview_type": payload.interview_type,
            "skills": skill_names,
            "resume_summary": candidate.resume_summary,
            "resume_raw": candidate.resume_raw,
        }
    )

    tavus_data: dict | None = None
    tavus_error: str | None = None
    conv_id: str | None = None
    conv_url: str | None = None
    try:
        tavus_data = tavus_service.create_conversation(
            conversation_name=f"InterviewDost Interview {interview.interview_id}",
            context=context_str,
        )

        if tavus_data:
            nested = tavus_data.get("data") if isinstance(tavus_data.get("data"), dict) else None
            conv_id = (
                tavus_data.get("conversation_id")
                or tavus_data.get("id")
                or (nested.get("conversation_id") if nested else None)
                or (nested.get("id") if nested else None)
            )
            conv_url = (
                tavus_data.get("conversation_url")
                or tavus_data.get("conversationUrl")
                or (nested.get("conversation_url") if nested else None)
                or (nested.get("conversationUrl") if nested else None)
            )

        if conv_id and not conv_url:
            try:
                detail = tavus_service.get_conversation(conv_id)
                nested_detail = detail.get("data") if isinstance(detail.get("data"), dict) else None
                conv_url = (
                    detail.get("conversation_url")
                    or detail.get("conversationUrl")
                    or (nested_detail.get("conversation_url") if nested_detail else None)
                    or (nested_detail.get("conversationUrl") if nested_detail else None)
                )
            except RuntimeError as e:
                logger.warning("Tavus conversation created but could not fetch details: %s", e)
    except RuntimeError as e:
        # If Tavus is unavailable or returns an error (e.g. rate limit, bad config),
        # continue with the interview flow but without an avatar URL. This keeps the
        # core product usable even when the external provider is flaky.
        tavus_error = str(e)
        tavus_data = None
        conv_id = None
        conv_url = None

    interview.tavus_conversation_id = conv_id
    interview.tavus_conversation_url = conv_url
    db.add(interview)
    db.commit()
    db.refresh(interview)

    # First question via Gemini service (currently stubbed for scoring pipeline)
    question_text = gemini_service.generate_question(candidate_profile)

    question = models.Question(
        interview_id=interview.interview_id,
        question_text=question_text,
    )
    db.add(question)
    db.commit()
    db.refresh(question)

    return schemas.InterviewStartResponse(
        interview_id=interview.interview_id,
        question=schemas.Question(
            question_id=question.question_id,
            text=question.question_text,
        ),
        conversation_url=interview.tavus_conversation_url,
        tavus_error=tavus_error,
    )


@router.post("/{interview_id}/questions/{question_id}/answer", response_model=schemas.AnswerResponse)
def submit_answer(
    interview_id: int,
    question_id: int,
    payload: schemas.AnswerRequest,
    db: Session = Depends(get_db),
):
    interview: Optional[models.Interview] = (
        db.query(models.Interview).filter_by(interview_id=interview_id).first()
    )
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    question: Optional[models.Question] = (
        db.query(models.Question)
        .filter_by(question_id=question_id, interview_id=interview_id)
        .first()
    )
    if not question:
        raise HTTPException(status_code=404, detail="Question not found for this interview")

    scores = gemini_service.evaluate_answer(question.question_text, payload.answer_text)

    response = models.Response(
        question_id=question.question_id,
        answer_text=payload.answer_text,
        relevance_score=scores["relevance_score"],
        confidence_level=scores["confidence_level"],
    )
    db.add(response)
    db.commit()
    db.refresh(response)

    # For now, compute overall_score from this single response
    interview.overall_score = int(
        (scores["relevance_score"] + scores["confidence_level"]) / 2
    )
    db.add(interview)
    db.commit()

    return schemas.AnswerResponse(
        interview_id=interview.interview_id,
        question_id=question.question_id,
        follow_up_question=None,
        done=True,
    )


@router.post("/{interview_id}/push-system-message")
def push_system_message(
    interview_id: int,
    payload: schemas.SystemMessageRequest,
    db: Session = Depends(get_db),
):
    interview: Optional[models.Interview] = (
        db.query(models.Interview).filter_by(interview_id=interview_id).first()
    )
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    if not interview.tavus_conversation_id:
        raise HTTPException(status_code=400, detail="No Tavus conversation linked")
    try:
        tavus_service.send_system_message(interview.tavus_conversation_id, payload.message)
        return {"status": "ok"}
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/{interview_id}/summary", response_model=schemas.InterviewSummaryResponse)
def get_summary(interview_id: int, db: Session = Depends(get_db)):
    interview: Optional[models.Interview] = (
        db.query(models.Interview).filter_by(interview_id=interview_id).first()
    )
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    questions = (
        db.query(models.Question)
        .filter_by(interview_id=interview_id)
        .order_by(models.Question.question_id)
        .all()
    )

    items: list[schemas.InterviewSummaryItem] = []
    for q in questions:
        resp = q.response
        items.append(
            schemas.InterviewSummaryItem(
                question=q.question_text,
                answer=resp.answer_text if resp else None,
                relevance_score=resp.relevance_score if resp else None,
                confidence_level=resp.confidence_level if resp else None,
            )
        )

    return schemas.InterviewSummaryResponse(
        interview_id=interview.interview_id,
        overall_score=interview.overall_score,
        items=items,
        completed_at=None,
    )


@router.post("/{interview_id}/feedback", response_model=dict)
def create_feedback(
    interview_id: int,
    comments: Optional[str] = None,
    suggestions: Optional[str] = None,
    report_url: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Create or update feedback for an interview.

    Later this can be auto-generated via Gemini based on all Q&A.
    """

    interview = db.query(models.Interview).filter_by(interview_id=interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    fb = db.query(models.Feedback).filter_by(interview_id=interview_id).first()
    if not fb:
        fb = models.Feedback(
            interview_id=interview_id,
            comments=comments,
            suggestions=suggestions,
            report_url=report_url,
        )
        db.add(fb)
    else:
        if comments is not None:
            fb.comments = comments
        if suggestions is not None:
            fb.suggestions = suggestions
        if report_url is not None:
            fb.report_url = report_url

    db.commit()
    db.refresh(fb)

    return {
        "feedback_id": fb.feedback_id,
        "interview_id": fb.interview_id,
        "comments": fb.comments,
        "suggestions": fb.suggestions,
        "report_url": fb.report_url,
    }


@router.get("/{interview_id}/feedback", response_model=dict)
def get_feedback(interview_id: int, db: Session = Depends(get_db)):
    fb = db.query(models.Feedback).filter_by(interview_id=interview_id).first()

    if not fb:
        interview = db.query(models.Interview).filter_by(interview_id=interview_id).first()
        if not interview:
            raise HTTPException(status_code=404, detail="Interview not found")

        # Build a simple structure for Gemini summary
        interview_info = {
            "candidate_name": interview.candidate.name if interview.candidate else None,
            "role": interview.type,
        }

        questions = (
            db.query(models.Question)
            .filter_by(interview_id=interview_id)
            .order_by(models.Question.question_id)
            .all()
        )

        qa_items: list[dict] = []
        for q in questions:
            resp = q.response
            qa_items.append(
                {
                    "question": q.question_text,
                    "answer": resp.answer_text if resp else None,
                }
            )

        summary = gemini_service.summarize_interview(interview_info, qa_items)

        fb = models.Feedback(
            interview_id=interview_id,
            comments=summary.get("comments"),
            suggestions=summary.get("suggestions"),
            report_url=None,
        )
        db.add(fb)
        db.commit()
        db.refresh(fb)

    return {
        "feedback_id": fb.feedback_id,
        "interview_id": fb.interview_id,
        "comments": fb.comments,
        "suggestions": fb.suggestions,
        "report_url": fb.report_url,
    }
