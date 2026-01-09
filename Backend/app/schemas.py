from datetime import datetime, date, time as time_type
from typing import Optional, List

from pydantic import BaseModel


class UserBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password_hash: Optional[str] = None
    role: Optional[str] = None
    resume_summary: Optional[str] = None


class User(UserBase):
    user_id: int

    class Config:
        from_attributes = True


class InterviewStartRequest(BaseModel):
    candidate: UserBase
    candidate_id: Optional[int] = None
    interviewer_id: Optional[int] = None
    interview_type: Optional[str] = None
    date: Optional[date] = None
    time: Optional[time_type] = None
    skills: Optional[List[str]] = None


class CandidateProfileInput(BaseModel):
    name: str
    email: str
    age: Optional[int] = None
    tech_stack: Optional[List[str]] = None
    work_experiences: Optional[List[str]] = None
    projects: Optional[List[str]] = None
    companies_worked: Optional[List[str]] = None
    target_role: Optional[str] = None
    target_company: Optional[str] = None
    resume_text: Optional[str] = None


class ProfileEnrichResponse(BaseModel):
    user_id: int
    resume_summary: str
    skills: List[str]

class AuthLoginRequest(BaseModel):
    email: str
    password: str


class AuthLoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: User


class Question(BaseModel):
    question_id: int
    text: str


class InterviewStartResponse(BaseModel):
    interview_id: int
    question: Question
    conversation_url: Optional[str] = None
    tavus_error: Optional[str] = None


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


class SystemMessageRequest(BaseModel):
    message: str

