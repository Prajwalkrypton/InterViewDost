from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..db import get_db
from ..services.gemini_service import gemini_service
from ..services.tavus_service import tavus_service

router = APIRouter()


# --- Routes -------------------------------------------------------------------


@router.post("/start", response_model=schemas.InterviewStartResponse)
def start_interview(payload: schemas.InterviewStartRequest, db: Session = Depends(get_db)):
    # Create candidate user (simple flow: always create a new user row)
    cand_data = payload.candidate
    candidate = models.User(
        name=cand_data.name,
        email=cand_data.email,
        password_hash=cand_data.password_hash,
        role=cand_data.role or "candidate",
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)

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
    }
    # You can later enrich this context with resume summary, skills, etc.
    context_str = (
        f"You are an AI interviewer. The candidate is {candidate_profile.get('name')} "
        f"for role {candidate_profile.get('role')}. Conduct a professional, structured "
        f"interview, starting with introductions and then exploring background, skills, "
        f"projects, and behavior."
    )

    try:
        tavus_data = tavus_service.create_conversation(
            conversation_name=f"InterviewDost Interview {interview.interview_id}",
            context=context_str,
        )
    except RuntimeError as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    interview.tavus_conversation_id = tavus_data.get("conversation_id")
    interview.tavus_conversation_url = tavus_data.get("conversation_url")
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
        raise HTTPException(status_code=404, detail="Feedback not found")

    return {
        "feedback_id": fb.feedback_id,
        "interview_id": fb.interview_id,
        "comments": fb.comments,
        "suggestions": fb.suggestions,
        "report_url": fb.report_url,
    }
