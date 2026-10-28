"""Modelos SQLAlchemy (RIF-01..RIF-05, RIN-02). Skeleton: esquema completo, SIN migraciones.

TODO (ROADMAP T-107): migraciones Alembic; T-108: repositorio Postgres que reemplace
`InMemorySessionStore`. Se usa JSON generico para correr tambien en SQLite (tests).
"""
from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):  # RIF-05: rol por usuario
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_hash: Mapped[str] = mapped_column(String(128), unique=True)   # nunca guardar email en claro
    role: Mapped[str] = mapped_column(String(16), default="student")    # student | expert | admin
    career: Mapped[str | None] = mapped_column(String(120))
    university: Mapped[str | None] = mapped_column(String(120))


class InterviewSession(Base):  # RIF-01
    __tablename__ = "interview_sessions"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    student_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    career: Mapped[str | None] = mapped_column(String(120))
    university: Mapped[str | None] = mapped_column(String(120))
    target_role: Mapped[str] = mapped_column(String(160))
    seniority: Mapped[str] = mapped_column(String(32))
    cv_text_anonymized: Mapped[str] = mapped_column(Text)               # RN-10
    job_description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="iniciada")  # SessionStatus
    max_turns: Mapped[int] = mapped_column(Integer, default=5)
    started_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    ended_at: Mapped[datetime | None] = mapped_column(DateTime)
    session_score: Mapped[float | None] = mapped_column(Float)
    score_evolution_rate: Mapped[float | None] = mapped_column(Float)
    report: Mapped[dict | None] = mapped_column(JSON)                   # RF-05 reporte almacenado
    turns: Mapped[list["MessageTurn"]] = relationship(back_populates="session")


class MessageTurn(Base):  # RIF-02
    __tablename__ = "message_turns"
    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("interview_sessions.id"))
    turn_number: Mapped[int] = mapped_column(Integer)                   # 1..10
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)
    is_followup: Mapped[bool] = mapped_column(default=False)
    length_chars: Mapped[int] = mapped_column(Integer)                  # RN-04
    length_words: Mapped[int] = mapped_column(Integer)
    metric_count: Mapped[int] = mapped_column(Integer)
    response_time_s: Mapped[float | None] = mapped_column(Float)
    session: Mapped[InterviewSession] = relationship(back_populates="turns")
    evaluation: Mapped["ModelEvaluation"] = relationship(back_populates="turn", uselist=False)


class ModelEvaluation(Base):  # RIF-03
    __tablename__ = "model_evaluations"
    id: Mapped[int] = mapped_column(primary_key=True)
    turn_id: Mapped[int] = mapped_column(ForeignKey("message_turns.id"))
    situacion: Mapped[int] = mapped_column(Integer)
    tarea: Mapped[int] = mapped_column(Integer)
    accion: Mapped[int] = mapped_column(Integer)
    resultado: Mapped[int] = mapped_column(Integer)
    claridad_tecnica: Mapped[int] = mapped_column(Integer)
    pertinencia: Mapped[int] = mapped_column(Integer)
    fortalezas: Mapped[list] = mapped_column(JSON, default=list)
    areas_mejora: Mapped[list] = mapped_column(JSON, default=list)
    is_weak: Mapped[bool] = mapped_column(default=False)
    improved_example: Mapped[str | None] = mapped_column(Text)
    prompt_version: Mapped[str | None] = mapped_column(String(32))      # trazabilidad MLOps (RN-11)
    turn: Mapped[MessageTurn] = relationship(back_populates="evaluation")


class UserFeedback(Base):  # RIF-04-1 (CSAT)
    __tablename__ = "user_feedback"
    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("interview_sessions.id"))
    csat: Mapped[int | None] = mapped_column(Integer)                   # 1..5
    comment: Mapped[str | None] = mapped_column(Text)
    abandon_reason: Mapped[str | None] = mapped_column(Text)


class GoldenDataset(Base):  # RIF-04-2
    __tablename__ = "golden_dataset"
    id: Mapped[int] = mapped_column(primary_key=True)
    career_area: Mapped[str] = mapped_column(String(120))               # estratificacion
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)
    rubric_id: Mapped[int | None] = mapped_column(ForeignKey("rubrics.id"))
    human_scores: Mapped[dict] = mapped_column(JSON)                    # 6 dimensiones
    model_scores: Mapped[dict | None] = mapped_column(JSON)
    hitl_status: Mapped[str] = mapped_column(String(24), default="pendiente")


class Rubric(Base):  # RF-08
    __tablename__ = "rubrics"
    id: Mapped[int] = mapped_column(primary_key=True)
    industry: Mapped[str] = mapped_column(String(120))
    kind: Mapped[str] = mapped_column(String(24))                       # conductual | tecnica
    content: Mapped[dict] = mapped_column(JSON)


class StudyResource(Base):  # RF-08 / RN-06
    __tablename__ = "study_resources"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    url: Mapped[str] = mapped_column(String(500))
    industry: Mapped[str | None] = mapped_column(String(120))
    tags: Mapped[list] = mapped_column(JSON, default=list)              # dimensiones STAR relacionadas
