import uuid
from app.extensions import db

class Integration(db.Model):
    __tablename__ = "integrations"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("organizations.id", ondelete="CASCADE"))
    provider_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default="not_connected")
    config = db.Column(db.JSON, default=dict)
    connected_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())