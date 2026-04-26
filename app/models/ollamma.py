import uuid
from app.extensions import db

class CandidateTranscript(db.Model):
    __tablename__ = "candidate_transcripts"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    candidate_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False
    )

    # interview / assessment session id (important for multiple rounds)
    session_id = db.Column(db.String(100), nullable=False)

    # full speech-to-text output
    transcript_text = db.Column(db.Text, nullable=False)

    # optional: AI summary from LLM (DeepSeek/Ollama)
    ai_summary = db.Column(db.Text)

    # optional: detected language (en, hi, etc.)
    language = db.Column(db.String(20), default="en")

    # timestamps
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )