import uuid
from app.extensions import db

class Candidate(db.Model):
    __tablename__ = "candidates"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("organizations.id", ondelete="CASCADE"))
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(30))
    location = db.Column(db.String(120))
    total_experience_years = db.Column(db.Numeric(4, 1))
    current_title = db.Column(db.String(150))
    current_company = db.Column(db.String(150))
    source = db.Column(db.String(50), default="manual")
    resume_url = db.Column(db.Text)
    linkedin_url = db.Column(db.Text)
    github_url = db.Column(db.Text)
    portfolio_url = db.Column(db.Text)
    summary = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

class CandidateSkill(db.Model):
    __tablename__ = "candidate_skills"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("candidates.id", ondelete="CASCADE"))
    skill_name = db.Column(db.String(120), nullable=False)