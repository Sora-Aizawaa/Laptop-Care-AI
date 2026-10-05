from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Category, Problem
from app.schemas.problem import CategoryOut, ProblemOut, ProblemSummary

router = APIRouter(tags=["knowledge-base"])


@router.get("/categories", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@router.get("/problems", response_model=list[ProblemSummary])
def list_problems(db: Session = Depends(get_db)):
    return db.query(Problem).all()


@router.get("/problems/{problem_id}", response_model=ProblemOut)
def get_problem(problem_id: int, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem
