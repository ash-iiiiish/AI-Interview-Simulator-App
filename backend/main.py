"""
main.py — FastAPI application entry point.

Run locally:
    cd backend
    uvicorn main:app --reload --port 8000
"""

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.routers import resume, interview, evaluation


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Auto-create all DB tables on startup
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="AI Interview Simulator API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume.router,     prefix="/api/resume",     tags=["Resume"])
app.include_router(interview.router,  prefix="/api/interview",  tags=["Interview"])
app.include_router(evaluation.router, prefix="/api/evaluation", tags=["Evaluation"])


@app.get("/")
async def root():
    return {"message": "AI Interview Simulator API is running 🚀"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
