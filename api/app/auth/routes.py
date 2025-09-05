"""Authentication routes."""

import uuid
from datetime import datetime, timedelta
from typing import Dict, Any
from flask import Blueprint, request, jsonify
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.db import get_db_session
from app.rcm.models import User

auth_bp = Blueprint("auth", __name__)


class LoginRequest(BaseModel):
    """Login request schema."""
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")


class LoginResponse(BaseModel):
    """Login response schema."""
    success: bool = Field(..., description="Login success status")
    message: str = Field(..., description="Response message")
    data: Dict[str, Any] = Field(default_factory=dict, description="User data")
    token: str = Field(..., description="Authentication token")
    trace_id: str = Field(..., description="Request trace ID")


class ErrorResponse(BaseModel):
    """Error response schema."""
    success: bool = Field(False, description="Success status")
    message: str = Field(..., description="Error message")
    error_code: str = Field(..., description="Error code")
    trace_id: str = Field(..., description="Request trace ID")


def generate_trace_id() -> str:
    """Generate unique trace ID."""
    return str(uuid.uuid4())


def generate_token(user_id: int) -> str:
    """Generate simple token for demo purposes."""
    return f"demo_token_{user_id}_{datetime.utcnow().timestamp()}"


@auth_bp.route("/login", methods=["POST"])
def login():
    """User login endpoint."""
    trace_id = generate_trace_id()
    
    try:
        # Validate request
        request_data = request.get_json()
        login_request = LoginRequest(**request_data)
        
        # Get database session
        db = get_db_session()
        
        # Find user by email
        user = db.query(User).filter(
            User.email == login_request.email,
            User.is_active == True
        ).first()
        
        if not user:
            return jsonify(ErrorResponse(
                success=False,
                message="Invalid email or password",
                error_code="INVALID_CREDENTIALS",
                trace_id=trace_id
            ).dict()), 401
        
        # For demo purposes, accept any password
        # In production, you would verify the password hash here
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        
        # Generate token
        token = generate_token(user.id)
        
        # Prepare response
        response = LoginResponse(
            success=True,
            message="Login successful",
            data={
                "user_id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "last_login": user.last_login.isoformat() if user.last_login else None
            },
            token=token,
            trace_id=trace_id
        )
        
        return jsonify(response.dict()), 200
        
    except Exception as e:
        return jsonify(ErrorResponse(
            success=False,
            message="Login failed",
            error_code="LOGIN_ERROR",
            trace_id=trace_id
        ).dict()), 500


@auth_bp.route("/verify", methods=["POST"])
def verify_token():
    """Verify authentication token."""
    trace_id = generate_trace_id()
    
    try:
        request_data = request.get_json()
        token = request_data.get("token")
        
        if not token:
            return jsonify(ErrorResponse(
                success=False,
                message="Token required",
                error_code="MISSING_TOKEN",
                trace_id=trace_id
            ).dict()), 400
        
        # For demo purposes, extract user ID from token
        # In production, you would verify JWT token here
        if token.startswith("demo_token_"):
            parts = token.split("_")
            if len(parts) >= 3:
                user_id = int(parts[2])
                
                # Get database session
                db = get_db_session()
                user = db.query(User).filter(
                    User.id == user_id,
                    User.is_active == True
                ).first()
                
                if user:
                    return jsonify({
                        "success": True,
                        "message": "Token valid",
                        "data": {
                            "user_id": user.id,
                            "email": user.email,
                            "name": user.name,
                            "role": user.role
                        },
                        "trace_id": trace_id
                    }), 200
        
        return jsonify(ErrorResponse(
            success=False,
            message="Invalid token",
            error_code="INVALID_TOKEN",
            trace_id=trace_id
        ).dict()), 401
        
    except Exception as e:
        return jsonify(ErrorResponse(
            success=False,
            message="Token verification failed",
            error_code="VERIFICATION_ERROR",
            trace_id=trace_id
        ).dict()), 500


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """User logout endpoint."""
    trace_id = generate_trace_id()
    
    try:
        # For demo purposes, just return success
        # In production, you would invalidate the token
        return jsonify({
            "success": True,
            "message": "Logout successful",
            "trace_id": trace_id
        }), 200
        
    except Exception as e:
        return jsonify(ErrorResponse(
            success=False,
            message="Logout failed",
            error_code="LOGOUT_ERROR",
            trace_id=trace_id
        ).dict()), 500
