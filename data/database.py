"""
Database Storage Layer for Career मार्ग.
Uses SQLite via SQLAlchemy for local persistence of candidate profiles,
job analysis sessions, interview logs, and career progress reports.
"""

import os
import json
from datetime import datetime
from typing import Optional, List, Dict, Any

from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class CandidateRecord(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    raw_text = Column(Text, nullable=True)
    profile_json = Column(Text, nullable=True)  # CandidateProfile serialized as JSON
    doc_analysis_json = Column(Text, nullable=True)


class JobAnalysisRecord(Base):
    __tablename__ = "job_analyses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, nullable=True)
    target_role = Column(String(255), nullable=True)
    job_description = Column(Text, nullable=True)
    ats_score = Column(Float, nullable=True)
    ats_result_json = Column(Text, nullable=True)
    skill_gap_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class InterviewRecord(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, nullable=True)
    session_id = Column(String(100), nullable=False)
    question = Column(Text, nullable=False)
    user_answer = Column(Text, nullable=True)
    overall_score = Column(Float, nullable=True)
    evaluation_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# Global Engine & Session Maker Initialization
DATABASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(DATABASE_DIR, exist_ok=True)
DATABASE_PATH = os.path.join(DATABASE_DIR, "careermarg.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    Initialize SQLite database tables.
    """
    Base.metadata.create_all(bind=engine)


def save_candidate_profile(filename: str, file_type: str, raw_text: str, profile_dict: dict, doc_analysis_dict: dict) -> int:
    """
    Save candidate profile record to database.
    """
    init_db()
    session = SessionLocal()
    try:
        rec = CandidateRecord(
            filename=filename,
            file_type=file_type,
            raw_text=raw_text,
            profile_json=json.dumps(profile_dict, default=str),
            doc_analysis_json=json.dumps(doc_analysis_dict, default=str)
        )
        session.add(rec)
        session.commit()
        session.refresh(rec)
        return rec.id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def save_job_analysis(candidate_id: Optional[int], target_role: str, job_description: str, ats_score: float, ats_result_dict: dict, skill_gap_dict: dict) -> int:
    """
    Save job analysis and ATS evaluation to database.
    """
    init_db()
    session = SessionLocal()
    try:
        rec = JobAnalysisRecord(
            candidate_id=candidate_id,
            target_role=target_role,
            job_description=job_description,
            ats_score=ats_score,
            ats_result_json=json.dumps(ats_result_dict, default=str),
            skill_gap_json=json.dumps(skill_gap_dict, default=str)
        )
        session.add(rec)
        session.commit()
        session.refresh(rec)
        return rec.id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def save_interview_turn(session_id: str, question: str, user_answer: str, score: float, eval_dict: dict, candidate_id: Optional[int] = None) -> int:
    """
    Save mock interview turn to database.
    """
    init_db()
    session = SessionLocal()
    try:
        rec = InterviewRecord(
            session_id=session_id,
            candidate_id=candidate_id,
            question=question,
            user_answer=user_answer,
            overall_score=score,
            evaluation_json=json.dumps(eval_dict, default=str)
        )
        session.add(rec)
        session.commit()
        session.refresh(rec)
        return rec.id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


init_db()
