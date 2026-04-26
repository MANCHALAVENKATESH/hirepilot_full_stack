import uuid
from app.extensions import db

class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("organizations.id", ondelete="CASCADE"))
    candidate_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("candidates.id", ondelete="CASCADE"))
    job_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("jobs.id", ondelete="CASCADE"))
    current_stage_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("pipeline_stages.id", ondelete="SET NULL"))
    status = db.Column(db.String(50), default="active")
    ai_match_score = db.Column(db.Numeric(5, 2))
    screening_score = db.Column(db.Numeric(5, 2))
    risk_level = db.Column(db.String(50))
    applied_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

class ApplicationStageHistory(db.Model):
    __tablename__ = "application_stage_history"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("applications.id", ondelete="CASCADE"))
    from_stage_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("pipeline_stages.id", ondelete="SET NULL"))
    to_stage_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("pipeline_stages.id", ondelete="SET NULL"))
    moved_by = db.Column(db.UUID(as_uuid=True), db.ForeignKey("users.id", ondelete="SET NULL"))
    moved_at = db.Column(db.DateTime, server_default=db.func.now())
    note = db.Column(db.Text)

class RecruiterNote(db.Model):
    __tablename__ = "recruiter_notes"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("applications.id", ondelete="CASCADE"))
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("users.id", ondelete="SET NULL"))
    note = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())