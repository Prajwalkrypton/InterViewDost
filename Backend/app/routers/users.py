from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models
from ..db import get_db

router = APIRouter()


@router.post("/", response_model=dict)
def create_user(
    name: Optional[str] = None,
    email: Optional[str] = None,
    password_hash: Optional[str] = None,
    role: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Create a basic user (candidate or interviewer).

    For now this uses simple query params / form fields for convenience.
    """

    user = models.User(
        name=name,
        email=email,
        password_hash=password_hash,
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"user_id": user.user_id}


@router.get("/{user_id}", response_model=dict)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(user_id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    skills = [
        {"skill_id": us.skill_id, "skill_name": us.skill.skill_name, "proficiency": us.proficiency}
        for us in user.user_skills
    ]

    return {
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "skills": skills,
    }


@router.post("/{user_id}/skills", response_model=dict)
def add_skills_to_user(
    user_id: int,
    skill_names: List[str],
    proficiencies: Optional[List[str]] = None,
    db: Session = Depends(get_db),
):
    """Attach one or more skills to a user.

    - skill_names: list of skill names (created if not existing)
    - proficiencies: optional list, same length as skill_names
    """

    user = db.query(models.User).filter_by(user_id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if proficiencies and len(proficiencies) != len(skill_names):
        raise HTTPException(status_code=400, detail="proficiencies length must match skill_names length")

    created = []
    for idx, name in enumerate(skill_names):
        skill = db.query(models.Skill).filter_by(skill_name=name).first()
        if not skill:
            skill = models.Skill(skill_name=name)
            db.add(skill)
            db.commit()
            db.refresh(skill)

        proficiency = None
        if proficiencies:
            proficiency = proficiencies[idx]

        link = db.query(models.UserSkill).filter_by(user_id=user_id, skill_id=skill.skill_id).first()
        if not link:
            link = models.UserSkill(user_id=user_id, skill_id=skill.skill_id, proficiency=proficiency)
            db.add(link)
        else:
            link.proficiency = proficiency
        created.append({"skill_id": skill.skill_id, "skill_name": skill.skill_name, "proficiency": proficiency})

    db.commit()

    return {"user_id": user_id, "skills": created}
