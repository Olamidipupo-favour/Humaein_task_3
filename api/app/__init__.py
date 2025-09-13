"""RCM GCC API - AI-Native Revenue Cycle Management Platform."""

import os
from typing import Optional
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from app.core.config import Config
from app.core.db import init_db
from app.rcm.routes import rcm_bp
from app.auth.routes import auth_bp

load_dotenv()


def create_app(config: Optional[Config] = None) -> Flask:
    """Create and configure Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    if config is None:
        config = Config()
    app.config.from_object(config)
    
    # Initialize extensions
    CORS(app, origins=config.ALLOW_ORIGINS)
    init_db(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(rcm_bp, url_prefix="/rcm")
    
    # Health check endpoint
    @app.route("/health")
    def health_check() -> dict:
        """Health check endpoint."""
        return jsonify({
            "status": "healthy",
            "service": "rcm-gcc-api",
            "version": "0.1.0"
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error) -> tuple[dict, int]:
        return jsonify({"error": "Not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(error) -> tuple[dict, int]:
        return jsonify({"error": "Internal server error"}), 500
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=True)