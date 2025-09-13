"""Authentication middleware and utilities."""

from functools import wraps
from typing import Optional, Dict, Any
from flask import request, jsonify
from sqlalchemy.orm import Session

from app.core.db import get_db_session
from app.rcm.models import User


import jwt
from app.core.config import Config

def get_current_user() -> Optional[User]:
    """Get current user from request token."""
    try:
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        
        # Decode JWT
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")

        if not user_id:
            return None

        # Get database session
        db = get_db_session()
        user = db.query(User).filter(
            User.id == user_id,
            User.is_active == True
        ).first()
        
        return user
        
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
    except Exception:
        return None


def require_auth(f):
    """Decorator to require authentication for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({
                "success": False,
                "message": "Authentication required",
                "error_code": "AUTH_REQUIRED"
            }), 401
        
        # Add user to kwargs for use in route
        kwargs['current_user'] = user
        return f(*args, **kwargs)
    
    return decorated_function


def require_role(required_role: str):
    """Decorator to require specific role for routes."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            if not user:
                return jsonify({
                    "success": False,
                    "message": "Authentication required",
                    "error_code": "AUTH_REQUIRED"
                }), 401
            
            if user.role != required_role and user.role != 'Admin':
                return jsonify({
                    "success": False,
                    "message": f"Role '{required_role}' required",
                    "error_code": "INSUFFICIENT_PERMISSIONS"
                }), 403
            
            kwargs['current_user'] = user
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
