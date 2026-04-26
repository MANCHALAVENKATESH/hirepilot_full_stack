import uuid
from app.extensions import db

class Organization(db.Model):
    __tablename__ = "organizations"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False)
    plan_name = db.Column(db.String(50), default="growth")
    default_region = db.Column(db.String(100))
    recruiting_email = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())