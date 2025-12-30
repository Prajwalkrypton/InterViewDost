from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import bcrypt

from .. import models, schemas
from ..db import get_db


router = APIRouter()


def hash_password(password: str) -> str:
    """Hash a password using bcrypt directly.

    This avoids Passlib's backend self-tests, which can be flaky on some
    Windows/Python combinations. The result is a UTF-8 string suitable for
    storing in the database.
    """

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
    except ValueError:
        # If the stored hash is somehow invalid, treat as non-match
        return False


@router.post("/auth/register_admin", response_model=schemas.User)
def register_admin(db: Session = Depends(get_db)):
    """One-time endpoint to create the admin user.

    Email and password are currently hardcoded as requested. If the user
    already exists, this simply returns the existing admin row.
    """

    email = "prajwalts.is23@rvce.edu.in"
    password = "1234"

    user = db.query(models.User).filter_by(email=email).first()
    if user:
        return user

    user = models.User(
        name="Prajwal",
        email=email,
        password_hash=hash_password(password),
        role="admin",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/auth/login", response_model=schemas.AuthLoginResponse)
def login(payload: schemas.AuthLoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(email=payload.email).first()
    if not user or not user.password_hash:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Simple opaque token for now; replace with real JWT later
    token = f"token-{user.user_id}"

    return schemas.AuthLoginResponse(
        access_token=token,
        token_type="bearer",
        user=schemas.User.model_validate(user),
    )
