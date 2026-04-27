import uuid
from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

class Candidate(db.Model):
    __tablename__ = "candidates"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = db.Column(UUID(as_uuid=True), db.ForeignKey("jobs.id"), nullable=False)

    full_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    experience = db.Column(db.String(100))
    skills = db.Column(db.JSON)
    summary = db.Column(db.Text)

    resume_filename = db.Column(db.String(255))
    resume_path = db.Column(db.String(500))

    ats_score = db.Column(db.Integer, default=0)
    match_score = db.Column(db.Integer, default=0)
    recommendation = db.Column(db.String(100), default="Suitable")

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    
class CandidateSkill(db.Model):
    __tablename__ = "candidate_skills"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("candidates.id", ondelete="CASCADE"))
    skill_name = db.Column(db.String(120), nullable=False)