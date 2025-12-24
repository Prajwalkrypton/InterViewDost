import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core_config import get_settings
from .db import Base, engine
from .routers import interview, users, health

settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup() -> None:
    # Create tables if they do not exist. In production, use Alembic migrations instead.
    Base.metadata.create_all(bind=engine)


app.include_router(interview.router, prefix="/api/interview", tags=["interview"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(health.router, tags=["health"])


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
