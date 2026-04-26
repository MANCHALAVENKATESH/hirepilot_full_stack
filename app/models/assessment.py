import uuid
from app.extensions import db

class Assessment(db.Model):
    __tablename__ = "assessments"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("organizations.id", ondelete="CASCADE"))
    job_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("jobs.id", ondelete="SET NULL"))
    created_by = db.Column(db.UUID(as_uuid=True), db.ForeignKey("users.id", ondelete="SET NULL"))
    name = db.Column(db.String(200), nullable=False)
    role_title = db.Column(db.String(200))
    difficulty = db.Column(db.String(50))
    duration_minutes = db.Column(db.Integer)
    total_questions = db.Column(db.Integer)
    assessment_kind = db.Column(db.String(50), default="coding")
    status = db.Column(db.String(50), default="draft")
    auto_send = db.Column(db.Boolean, default=False)
    webcam_monitoring = db.Column(db.Boolean, default=True)
    tab_switch_detection = db.Column(db.Boolean, default=True)
    copy_paste_blocking = db.Column(db.Boolean, default=True)
    multiple_face_detection = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

class AssessmentQuestion(db.Model):
    __tablename__ = "assessment_questions"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("assessments.id", ondelete="CASCADE"))
    question_order = db.Column(db.Integer, nullable=False)
    question_type = db.Column(db.String(50), default="coding")
    title = db.Column(db.String(255), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    example_input = db.Column(db.Text)
    example_output = db.Column(db.Text)
    constraints_text = db.Column(db.Text)
    ai_explanation_prompt = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class AssessmentSubmission(db.Model):
    __tablename__ = "assessment_submissions"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("assessments.id", ondelete="CASCADE"))
    application_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("applications.id", ondelete="CASCADE"))
    candidate_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("candidates.id", ondelete="CASCADE"))
    status = db.Column(db.String(50), default="not_sent")
    language = db.Column(db.String(50))
    started_at = db.Column(db.DateTime)
    submitted_at = db.Column(db.DateTime)
    score = db.Column(db.Numeric(5, 2))
    passed_visible_tests = db.Column(db.Boolean)
    tab_switch_count = db.Column(db.Integer, default=0)
    integrity_flags = db.Column(db.JSON, default=list)
    output_summary = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

class AssessmentAnswer(db.Model):
    __tablename__ = "assessment_answers"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    submission_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("assessment_submissions.id", ondelete="CASCADE"))
    question_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("assessment_questions.id", ondelete="CASCADE"))
    answer_text = db.Column(db.Text)
    code_text = db.Column(db.Text)
    output_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())