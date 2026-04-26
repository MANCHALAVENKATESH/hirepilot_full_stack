from flask import Flask
from app.config import Config
from app.extensions import db, migrate, jwt, cors

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(
    app,
    resources={r"/*": {"origins": "http://localhost:5173"}},
    supports_credentials=True
)
    from app import models

    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.jobs import jobs_bp
    from app.routes.candidates import candidates_bp
    from app.routes.pipeline import pipeline_bp
    from app.routes.assessments import assessments_bp
    from app.routes.notifications import notifications_bp
    from app.routes.analytics import analytics_bp
    from app.routes.settings import settings_bp
    from app.routes.integrations import integrations_bp
    from app.routes.ollamma import candidate_transcript

    app.register_blueprint(auth_bp, url_prefix="/register")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
    app.register_blueprint(jobs_bp, url_prefix="/api/jobs")
    app.register_blueprint(candidates_bp, url_prefix="/api/candidates")
    app.register_blueprint(pipeline_bp, url_prefix="/api/pipeline")
    app.register_blueprint(assessments_bp, url_prefix="/api/assessments")
    app.register_blueprint(notifications_bp, url_prefix="/api/notifications")
    app.register_blueprint(analytics_bp, url_prefix="/api/analytics")
    app.register_blueprint(settings_bp, url_prefix="/api/settings")
    app.register_blueprint(integrations_bp, url_prefix="/api/integrations")
    app.register_blueprint(candidate_transcript)

    @app.route("/")
    def home():
        return {"message": "HirePilot Flask API is running"}

    return app