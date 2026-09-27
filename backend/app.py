import os

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from backend.config import Config

from backend.routes.auth import auth_bp
from backend.routes.health_reports import health_reports_bp
from backend.routes.uploads import uploads_bp
from backend.routes.investigations import investigations_bp
from backend.routes.laboratory import laboratory_bp
from backend.routes.dashboard import dashboard_bp
from backend.routes.clusters import clusters_bp
from backend.routes.notifications import notifications_bp


# ============================================================
# APPLICATION SETUP
# ============================================================

app = Flask(__name__)
app.config.from_object(Config)


# ============================================================
# FRONTEND PATH
# ============================================================

FRONTEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "frontend")
)


# ============================================================
# CORS
# ============================================================

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": "*"
        }
    },
    supports_credentials=False,
)


# ============================================================
# JWT
# ============================================================

jwt = JWTManager(app)


# ============================================================
# BLUEPRINTS
# ============================================================

app.register_blueprint(auth_bp)
app.register_blueprint(health_reports_bp)
app.register_blueprint(uploads_bp)
app.register_blueprint(investigations_bp)
app.register_blueprint(laboratory_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(clusters_bp)
app.register_blueprint(notifications_bp)


# ============================================================
# FRONTEND
# ============================================================

@app.route("/", methods=["GET"])
def frontend_home():
    """
    Serve the main Uyirthulir frontend.
    """
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:path>", methods=["GET"])
def frontend_files(path):
    """
    Serve frontend files such as CSS, JavaScript, images,
    and HTML pages.
    """

    file_path = os.path.join(FRONTEND_DIR, path)

    if os.path.isfile(file_path):
        return send_from_directory(FRONTEND_DIR, path)

    # If the requested frontend route doesn't directly exist,
    # return the main frontend page.
    return send_from_directory(FRONTEND_DIR, "index.html")


# ============================================================
# API ROOT
# ============================================================

@app.route("/api", methods=["GET"])
def api_home():
    return jsonify(
        {
            "success": True,
            "name": "AI-Enabled Livestock Health Early-Warning & Surveillance Platform",
            "version": "1.0.0",
            "status": "running",
            "modules": {
                "authentication": "/api/auth",
                "healthReports": "/api/health-reports",
                "uploads": "/api/uploads",
                "investigations": "/api/investigations",
                "laboratory": "/api/laboratory",
                "dashboard": "/api/dashboard",
                "clusters": "/api/clusters",
                "notifications": "/api/notifications",
            },
        }
    ), 200


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify(
        {
            "success": True,
            "status": "healthy",
            "service": "livestock-health-platform",
        }
    ), 200


# ============================================================
# 404 HANDLER
# ============================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify(
        {
            "success": False,
            "message": "API endpoint not found.",
        }
    ), 404


# ============================================================
# 500 HANDLER
# ============================================================

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify(
        {
            "success": False,
            "message": "Internal server error.",
        }
    ), 500


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )