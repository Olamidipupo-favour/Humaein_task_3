"""RCM API routes."""

import uuid
from datetime import datetime
from typing import Dict, Any
from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from app.core.schemas import (
    EligibilityRequest, EligibilityResponse,
    PriorAuthRequest, PriorAuthResponse,
    CodingRequest, CodingResponse,
    ScrubbingRequest, ScrubbingResponse,
    ClaimsSubmissionRequest, ClaimsSubmissionResponse,
    RemittanceResponse,
    DenialAppealRequest, DenialAppealResponse,
    ErrorResponse
)
from app.core.db import get_db_session
from app.core.auth import require_auth
from app.rcm.services import RCMService

rcm_bp = Blueprint("rcm", __name__)


def generate_trace_id() -> str:
    """Generate unique trace ID."""
    return str(uuid.uuid4())


@rcm_bp.route("/eligibility/check", methods=["POST"])
def check_eligibility():
    """Check patient eligibility."""
    trace_id = generate_trace_id()
    
    try:
        # Validate request
        request_data = request.get_json()
        eligibility_request = EligibilityRequest(**request_data)
        
        # Get database session
        db = get_db_session()
        rcm_service = RCMService(db)
        
        # Process eligibility check
        result = rcm_service.check_eligibility(
            patient_id=eligibility_request.patient_id,
            payer_id=eligibility_request.payer_id,
            service_date=eligibility_request.service_date,
            service_type=eligibility_request.service_type
        )
        
        if "error" in result:
            return jsonify(ErrorResponse(
                success=False,
                message=result["error"],
                trace_id=trace_id
            ).dict()), 400
        
        # Prepare response
        response = EligibilityResponse(
            data=result,
            ai_suggestions=result.get("suggestions", []),
            trace_id=trace_id
        )
        
        return jsonify(response.dict()), 200
        
    except ValidationError as e:
        return jsonify(ErrorResponse(
            success=False,
            message="Validation error",
            error_code="VALIDATION_ERROR",
            details={"errors": e.errors()},
            trace_id=trace_id
        ).dict()), 400
    except Exception as e:
        return jsonify(ErrorResponse(
            success=False,
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            trace_id=trace_id
        ).dict()), 500


@rcm_bp.route("/prior-auth/draft", methods=["POST"])
def draft_prior_auth():
    """Generate prior authorization draft."""
    trace_id = generate_trace_id()
    
    try:
        # Validate request
        request_data = request.get_json()
        prior_auth_request = PriorAuthRequest(**request_data)
        
        # Get database session
        db = get_db_session()
        rcm_service = RCMService(db)
        
        # Process prior auth generation
        result = rcm_service.generate_prior_auth(
            patient_id=prior_auth_request.patient_id,
            service_type=prior_auth_request.service_type,
            diagnosis_codes=prior_auth_request.diagnosis_codes,
            clinical_notes=prior_auth_request.clinical_notes
        )
        
        if "error" in result:
            return jsonify(ErrorResponse(
                success=False,
                message=result["error"],
                trace_id=trace_id
            ).dict()), 400
        
        # Prepare response
        response = PriorAuthResponse(
            data=result,
            checklist=result.get("checklist", []),
            draft_letter=result.get("draft_letter"),
            trace_id=trace_id
        )
        
        return jsonify(response.dict()), 200
        
    except ValidationError as e:
        return jsonify(ErrorResponse(
            success=False,
            message="Validation error",
            error_code="VALIDATION_ERROR",
            details={"errors": e.errors()},
            trace_id=trace_id
        ).dict()), 400
    except Exception as e:
        return jsonify(ErrorResponse(
            success=False,
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            trace_id=trace_id
        ).dict()), 500


@rcm_bp.route("/coding/suggest", methods=["POST"])
def suggest_coding():
    """Suggest medical coding."""
    trace_id = generate_trace_id()
    
    try:
        # Validate request
        request_data = request.get_json()
        coding_request = CodingRequest(**request_data)
        
        # Get database session
        db = get_db_session()
        rcm_service = RCMService(db)
        
        # Process coding suggestion
        result = rcm_service.suggest_coding(
            clinical_notes=coding_request.clinical_notes,
            service_type=coding_request.service_type,
            provider_specialty=coding_request.provider_specialty
        )
        
        # Prepare response
        response = CodingResponse(
            data=result,
            icd_codes=result.get("icd_codes", []),
            cpt_codes=result.get("cpt_codes", []),
            rationale=result.get("rationale", ""),
            trace_id=trace_id
        )
        
        return jsonify(response.dict()), 200
        
    except ValidationError as e:
        print(e)
        return jsonify(ErrorResponse(
            success=False,
            message="Validation error",
            error_code="VALIDATION_ERROR",
            details={"errors": e.errors()},
            trace_id=trace_id
        ).dict()), 400
    except Exception as e:
        return jsonify(ErrorResponse(
            success=False,
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            trace_id=trace_id
        ).dict()), 500


@rcm_bp.route("/scrub", methods=["POST"])
def scrub_claim():
    """Scrub claim for issues."""
    trace_id = generate_trace_id()
    
    try:
        # Validate request
        request_data = request.get_json()
        scrubbing_request = ScrubbingRequest(**request_data)
        
        # Get database session
        db = get_db_session()
        rcm_service = RCMService(db)
        
        # Process claim scrubbing
        result = rcm_service.scrub_claim(
            claim_data=scrubbing_request.claim_data,
            payer_rules=scrubbing_request.payer_rules
        )
        
        # Prepare response
        response = ScrubbingResponse(
            data=result,
            issues=result.get("issues", []),
            recommendations=result.get("recommendations", []),
            trace_id=trace_id
        )
        
        return jsonify(response.dict()), 200
        
    except ValidationError as e:
        return jsonify(ErrorResponse(
            success=False,
            message="Validation error",
            error_code="VALIDATION_ERROR",
            details={"errors": e.errors()},
            trace_id=trace_id
        ).dict()), 400
    except Exception as e:
        return jsonify(ErrorResponse(
            success=False,
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            trace_id=trace_id
        ).dict()), 500


@rcm_bp.route("/claims/submit", methods=["POST"])
def submit_claim():
    """Submit claim to payer."""
    trace_id = generate_trace_id()
    
    try:
        # Validate request
        request_data = request.get_json()
        submission_request = ClaimsSubmissionRequest(**request_data)
        
        # Get database session
        db = get_db_session()
        rcm_service = RCMService(db)
        
        # Process claim submission
        result = rcm_service.submit_claim(
            claim_data=submission_request.claim_data,
            payer_id=submission_request.payer_id
        )
        
        # Prepare response
        response = ClaimsSubmissionResponse(
            data=result,
            claim_id=result.get("claim_id", ""),
            status=result.get("status", ""),
            trace_id=trace_id
        )
        
        return jsonify(response.dict()), 200
        
    except ValidationError as e:
        return jsonify(ErrorResponse(
            success=False,
            message="Validation error",
            error_code="VALIDATION_ERROR",
            details={"errors": e.errors()},
            trace_id=trace_id
        ).dict()), 400
    except Exception as e:
        return jsonify(ErrorResponse(
            success=False,
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            trace_id=trace_id
        ).dict()), 500


@rcm_bp.route("/remittance/<claim_id>", methods=["GET"])
def get_remittance(claim_id: str):
    """Get remittance information."""
    trace_id = generate_trace_id()
    
    try:
        # Get database session
        db = get_db_session()
        rcm_service = RCMService(db)
        
        # Get remittance data
        result = rcm_service.get_remittance(claim_id)
        
        # Prepare response
        response = RemittanceResponse(
            data=result,
            payments=result.get("payments", []),
            adjustments=result.get("adjustments", []),
            trace_id=trace_id
        )
        
        return jsonify(response.dict()), 200
        
    except Exception as e:
        return jsonify(ErrorResponse(
            success=False,
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            trace_id=trace_id
        ).dict()), 500


@rcm_bp.route("/denials/appeal", methods=["POST"])
def appeal_denial():
    """Appeal claim denial."""
    trace_id = generate_trace_id()
    
    try:
        # Validate request
        request_data = request.get_json()
        appeal_request = DenialAppealRequest(**request_data)
        
        # Get database session
        db = get_db_session()
        rcm_service = RCMService(db)
        
        # Process denial appeal
        result = rcm_service.appeal_denial(
            denial_id=appeal_request.denial_id,
            appeal_reason=appeal_request.appeal_reason,
            additional_docs=appeal_request.additional_docs
        )
        
        if "error" in result:
            return jsonify(ErrorResponse(
                success=False,
                message=result["error"],
                trace_id=trace_id
            ).dict()), 400
        
        # Prepare response
        response = DenialAppealResponse(
            data=result,
            appeal_id=result.get("appeal_id", ""),
            next_steps=result.get("next_steps", []),
            ai_analysis=result.get("analysis"),
            trace_id=trace_id
        )
        
        return jsonify(response.dict()), 200
        
    except ValidationError as e:
        return jsonify(ErrorResponse(
            success=False,
            message="Validation error",
            error_code="VALIDATION_ERROR",
            details={"errors": e.errors()},
            trace_id=trace_id
        ).dict()), 400
    except Exception as e:
        return jsonify(ErrorResponse(
            success=False,
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            trace_id=trace_id
        ).dict()), 500


@rcm_bp.route("/dashboard/stats", methods=["GET"])
@require_auth
def get_dashboard_stats(current_user):
    """Get dashboard statistics."""
    trace_id = generate_trace_id()
    
    try:
        # Get database session
        db = get_db_session()
        rcm_service = RCMService(db)
        
        # Get dashboard stats for the current user
        stats = rcm_service.get_dashboard_stats(user_id=current_user.id)
        
        return jsonify({
            "success": True,
            "data": stats,
            "trace_id": trace_id
        }), 200
        
    except Exception as e:
        return jsonify(ErrorResponse(
            success=False,
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            trace_id=trace_id
        ).dict()), 500
