from datetime import date

from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text, Time
from sqlalchemy.orm import relationship

from .db import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    email = Column(String(255), nullable=True, unique=True)
    password_hash = Column(String(255), nullable=True)
    role = Column(String(50), nullable=True)  # e.g., "candidate", "interviewer", "admin"
    resume_summary = Column(Text, nullable=True)

    # Relationships
    candidate_interviews = relationship(
        "Interview",
        back_populates="candidate",
        foreign_keys="Interview.candidate_id",
    )
    interviewer_interviews = relationship(
        "Interview",
        back_populates="interviewer",
        foreign_keys="Interview.interviewer_id",
    )
    user_skills = relationship("UserSkill", back_populates="user", cascade="all, delete-orphan")


class Skill(Base):
    __tablename__ = "skills"

    skill_id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String(100), nullable=False, unique=True)

    user_skills = relationship("UserSkill", back_populates="skill", cascade="all, delete-orphan")


class UserSkill(Base):
    __tablename__ = "user_skills"

    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.skill_id"), primary_key=True)
    proficiency = Column(String(50), nullable=True)

    user = relationship("User", back_populates="user_skills")
    skill = relationship("Skill", back_populates="user_skills")


class Interview(Base):
    __tablename__ = "interviews"

    interview_id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    interviewer_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    date = Column(Date, nullable=True)
    time = Column(Time, nullable=True)
    type = Column(String(100), nullable=True)
    overall_score = Column(Integer, nullable=True)
    tavus_conversation_id = Column(String(100), nullable=True)
    tavus_conversation_url = Column(String(255), nullable=True)

    candidate = relationship("User", foreign_keys=[candidate_id], back_populates="candidate_interviews")
    interviewer = relationship("User", foreign_keys=[interviewer_id], back_populates="interviewer_interviews")
    questions = relationship("Question", back_populates="interview", cascade="all, delete-orphan")
    feedback = relationship("Feedback", back_populates="interview", uselist=False, cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(100), nullable=False, unique=True)

    questions = relationship("Question", back_populates="category")


class Question(Base):
    __tablename__ = "questions"

    question_id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.interview_id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=True)
    question_text = Column(Text, nullable=False)

    interview = relationship("Interview", back_populates="questions")
    category = relationship("Category", back_populates="questions")
    response = relationship("Response", back_populates="question", uselist=False, cascade="all, delete-orphan")


class Response(Base):
    __tablename__ = "responses"

    response_id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.question_id"), nullable=False, unique=True)
    answer_text = Column(Text, nullable=True)
    relevance_score = Column(Integer, nullable=True)
    confidence_level = Column(Integer, nullable=True)

    question = relationship("Question", back_populates="response")


class Feedback(Base):
    __tablename__ = "feedbacks"

    feedback_id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.interview_id"), nullable=False, unique=True)
    comments = Column(Text, nullable=True)
    suggestions = Column(Text, nullable=True)
    report_url = Column(String(255), nullable=True)

    interview = relationship("Interview", back_populates="feedback")

