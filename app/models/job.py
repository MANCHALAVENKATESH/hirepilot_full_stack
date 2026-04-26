import uuid
from app.extensions import db

class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("organizations.id", ondelete="CASCADE"))
    created_by = db.Column(db.UUID(as_uuid=True), db.ForeignKey("users.id", ondelete="SET NULL"))
    title = db.Column(db.String(200), nullable=False)
    department = db.Column(db.String(120))
    location = db.Column(db.String(120))
    employment_type = db.Column(db.String(80))
    experience_min = db.Column(db.Integer)
    experience_max = db.Column(db.Integer)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default="draft")
    ai_matching_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

class JobSkill(db.Model):
    __tablename__ = "job_skills"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("jobs.id", ondelete="CASCADE"))
    skill_name = db.Column(db.String(120), nullable=False)

class PipelineStage(db.Model):
    __tablename__ = "pipeline_stages"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("organizations.id", ondelete="CASCADE"))
    job_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("jobs.id", ondelete="CASCADE"))
    stage_name = db.Column(db.String(100), nullable=False)
    stage_order = db.Column(db.Integer, nullable=False)
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())