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


@rcm_bp.route("/claims/scrub", methods=["POST"])
def scrub_claim_route():
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


@rcm_bp.route("/claims/track/<claim_id>", methods=["GET"])
def track_claim(claim_id: str):
    """Track claim status."""
    trace_id = generate_trace_id()
    
    try:
        # Get database session
        db = get_db_session()
        rcm_service = RCMService(db)
        
        # Get claim status
        result = rcm_service.track_claim(claim_id)
        
        if "error" in result:
            return jsonify(ErrorResponse(
                success=False,
                message=result["error"],
                trace_id=trace_id
            ).dict()), 404
        
        return jsonify({
            "success": True,
            "data": result,
            "trace_id": trace_id
        }), 200
        
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


@rcm_bp.route("/analytics/revenue", methods=["GET"])
@require_auth
def get_revenue_analytics(current_user):
    """Get revenue analytics data."""
    trace_id = generate_trace_id()
    
    try:
        # Get database session
        db = get_db_session()
        rcm_service = RCMService(db)
        
        # Get revenue analytics
        analytics = rcm_service.get_revenue_analytics(user_id=current_user.id)
        
        return jsonify({
            "success": True,
            "data": analytics,
            "trace_id": trace_id
        }), 200
        
    except Exception as e:
        return jsonify(ErrorResponse(
            success=False,
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            trace_id=trace_id
        ).dict()), 500


@rcm_bp.route("/analytics/denials", methods=["GET"])
@require_auth
def get_denial_analytics(current_user):
    """Get denial analytics data."""
    trace_id = generate_trace_id()
    
    try:
        # Get database session
        db = get_db_session()
        rcm_service = RCMService(db)
        
        # Get denial analytics
        analytics = rcm_service.get_denial_analytics(user_id=current_user.id)
        
        return jsonify({
            "success": True,
            "data": analytics,
            "trace_id": trace_id
        }), 200
        
    except Exception as e:
        return jsonify(ErrorResponse(
            success=False,
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            trace_id=trace_id
        ).dict()), 500


@rcm_bp.route("/payers", methods=["GET"])
def get_payers():
    """Get a list of payers."""
    trace_id = generate_trace_id()
    
    try:
        payers = [
            { "id": "1", "name": "Blue Cross Blue Shield" },
            { "id": "2", "name": "Aetna" },
            { "id": "3", "name": "Cigna" },
            { "id": "4", "name": "UnitedHealth" },
            { "id": "5", "name": "Medicare" },
        ]
        
        return jsonify({
            "success": True,
            "data": payers,
            "trace_id": trace_id
        }), 200
        
    except Exception as e:
        return jsonify(ErrorResponse(
            success=False,
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            trace_id=trace_id
        ).dict()), 500


@rcm_bp.route("/recent-activity", methods=["GET"])
@require_auth
def get_recent_activity(current_user):
    """Get recent activity."""
    trace_id = generate_trace_id()
    
    try:
        # Get database session
        db = get_db_session()
        rcm_service = RCMService(db)
        
        # Get recent activity from database
        activities = rcm_service.get_recent_activity(user_id=current_user.id)
        
        return jsonify({
            "success": True,
            "data": activities,
            "trace_id": trace_id
        }), 200
        
    except Exception as e:
        return jsonify(ErrorResponse(
            success=False,
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            trace_id=trace_id
        ).dict()), 500


@rcm_bp.route("/analytics/kpis", methods=["GET"])
@require_auth
def get_kpis(current_user):
    """Get a list of KPIs."""
    trace_id = generate_trace_id()
    
    try:
        # Get database session
        db = get_db_session()
        rcm_service = RCMService(db)
        
        # Get dashboard stats for KPIs
        stats = rcm_service.get_dashboard_stats(user_id=current_user.id)
        
        # Calculate growth rates (simplified for demo)
        revenue_growth = 12.5  # This would be calculated from historical data
        clean_claim_rate_change = 2.1  # This would be calculated from historical data
        
        kpis = {
            "revenue_growth": {
                "value": f"+{revenue_growth}%",
                "change": f"+${stats.get('total_revenue', 0) * 0.1:.0f}K",
                "changeType": "positive",
            },
            "clean_claim_rate": {
                "value": f"{stats.get('clean_claim_rate', 0)}%",
                "change": f"+{clean_claim_rate_change}%",
                "changeType": "positive",
            },
            "avg_days_to_payment": {
                "value": f"{stats.get('avg_days_to_payment', 0)} days",
                "change": "-3 days",
                "changeType": "positive",
            },
            "denial_rate": {
                "value": f"{stats.get('denial_rate', 0)}%",
                "change": "-1.2%",
                "changeType": "positive",
            },
            "first_pass_success_rate": {
                "value": f"{stats.get('clean_claim_rate', 0)}%",
                "change": f"+{clean_claim_rate_change}% from last month",
            },
            "avg_days_to_payment_kpi": {
                "value": f"{stats.get('avg_days_to_payment', 0)}",
                "change": "-3 days improvement",
            },
            "monthly_revenue": {
                "value": f"${stats.get('total_revenue', 0):,.0f}",
                "change": f"+{revenue_growth}% growth",
            },
        }
        
        return jsonify({
            "success": True,
            "data": kpis,
            "trace_id": trace_id
        }), 200
        
    except Exception as e:
        return jsonify(ErrorResponse(
            success=False,
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            trace_id=trace_id
        ).dict()), 500


@rcm_bp.route("/seed-demo-data", methods=["POST"])
@require_auth
def seed_demo_data(current_user):
    """Seed demo data for testing."""
    trace_id = generate_trace_id()
    
    try:
        # Get database session
        db = get_db_session()
        
        # Create some sample claims for the last 6 months
        from datetime import datetime, timedelta
        import random
        from app.rcm.models import Claim, ClaimStatus, Patient, Provider, Payer, Encounter
        
        # Get or create sample entities
        patient = db.query(Patient).first()
        provider = db.query(Provider).first()
        payer = db.query(Payer).first()
        
        if not patient:
            patient = Patient(
                first_name="Demo",
                last_name="Patient",
                date_of_birth=datetime(1980, 1, 1),
                gender="Male",
                insurance_id="DEMO-001",
                address="123 Demo Street",
                phone="+966-50-123-4567",
                email="demo@patient.com"
            )
            db.add(patient)
            db.flush()  # Use flush instead of commit to get the ID
        
        if not provider:
            provider = Provider(
                name="Dr. Demo Provider",
                npi="1234567890",
                specialty="General Practice",
                address="456 Medical Center",
                phone="+966-11-123-4567",
                email="demo@provider.com"
            )
            db.add(provider)
            db.flush()  # Use flush instead of commit to get the ID
        
        if not payer:
            payer = Payer(
                name="Demo Insurance",
                payer_id="DEMO-INS-001",
                payer_type="Private",
                address="789 Insurance Plaza",
                phone="+966-11-987-6543",
                email="demo@insurance.com"
            )
            db.add(payer)
            db.flush()  # Use flush instead of commit to get the ID
        
        # Create claims for the last 6 months
        current_date = datetime.utcnow()
        claims_created = 0
        for i in range(6):
            month_start = current_date.replace(day=1) - timedelta(days=30 * i)
            for j in range(random.randint(5, 15)):  # 5-15 claims per month
                claim_date = month_start + timedelta(days=random.randint(1, 28))
                
                # Create an encounter for each claim
                encounter = Encounter(
                    encounter_date=claim_date,
                    encounter_type=random.choice(["Inpatient", "Outpatient", "Emergency"]),
                    diagnosis_codes='["E11.9"]',  # JSON string
                    procedure_codes='["99213"]',  # JSON string
                    clinical_notes=f"Demo encounter for claim {j}",
                    patient_id=patient.id,
                    provider_id=provider.id
                )
                db.add(encounter)
                db.flush()  # Get the encounter ID
                
                claim = Claim(
                    claim_id=f"DEMO-{claim_date.strftime('%Y%m%d')}-{random.randint(1000, 9999)}",
                    claim_date=claim_date,
                    service_date=claim_date,
                    total_amount=round(random.uniform(200.0, 1500.0), 2),
                    status=random.choice(list(ClaimStatus)),
                    submission_date=claim_date + timedelta(days=1),
                    patient_id=patient.id,
                    provider_id=provider.id,
                    payer_id=payer.id,
                    encounter_id=encounter.id
                )
                db.add(claim)
                claims_created += 1
        
        db.commit()
        
        return jsonify({
            "success": True,
            "message": f"Demo data seeded successfully. Created {claims_created} claims.",
            "claims_created": claims_created,
            "trace_id": trace_id
        }), 200
        
    except Exception as e:
        print(f"Error in seed_demo_data: {str(e)}")  # Debug logging
        db.rollback()  # Rollback on error
        return jsonify(ErrorResponse(
            success=False,
            message=f"Internal server error: {str(e)}",
            error_code="INTERNAL_ERROR",
            trace_id=trace_id
        ).dict()), 500
