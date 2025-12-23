from datetime import datetime, date, time as time_type
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password_hash: Optional[str] = None
    role: Optional[str] = None


class User(UserBase):
    user_id: int

    class Config:
        from_attributes = True


class InterviewStartRequest(BaseModel):
    candidate: UserBase
    interviewer_id: Optional[int] = None
    interview_type: Optional[str] = None
    date: Optional[date] = None
    time: Optional[time_type] = None


class Question(BaseModel):
    question_id: int
    text: str


class InterviewStartResponse(BaseModel):
    interview_id: int
    question: Question


class AnswerRequest(BaseModel):
    answer_text: str


class AnswerResponse(BaseModel):
    interview_id: int
    question_id: int
    follow_up_question: Optional[Question] = None
    done: bool


class InterviewSummaryItem(BaseModel):
    question: str
    answer: Optional[str]
    relevance_score: Optional[int]
    confidence_level: Optional[int]


class InterviewSummaryResponse(BaseModel):
    interview_id: int
    overall_score: Optional[int]
    items: list[InterviewSummaryItem]
    completed_at: Optional[datetime]

