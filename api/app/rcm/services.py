"""Business logic services for RCM workflows."""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session

from app.rcm.models import (
    Provider, Payer, Patient, Encounter, Claim, ClaimLine, 
    Remittance, Denial, User, ClaimStatus, DenialReason
)
from app.ai.chains import ai_chains


class RCMService:
    """RCM business logic service."""
    
    def __init__(self, db: Session):
        """Initialize service with database session."""
        self.db = db
    
    def check_eligibility(self, patient_id: str, payer_id: str, service_date: datetime, service_type: str) -> Dict[str, Any]:
        """Check patient eligibility for service."""
        # Get patient and payer data
        patient = self.db.query(Patient).filter(Patient.insurance_id == patient_id).first()
        payer = self.db.query(Payer).filter(Payer.payer_id == payer_id).first()
        
        if not patient or not payer:
            return {"error": "Patient or payer not found"}
        
        # Prepare data for AI analysis
        patient_data = {
            "id": patient.insurance_id,
            "name": f"{patient.first_name} {patient.last_name}",
            "dob": patient.date_of_birth.strftime("%Y-%m-%d"),
            "gender": patient.gender
        }
        
        payer_data = {
            "id": payer.payer_id,
            "name": payer.name,
            "type": payer.payer_type
        }
        
        # Get AI analysis
        ai_result = ai_chains.eligibility_chain(patient_data, payer_data)
        
        return {
            "patient": patient_data,
            "payer": payer_data,
            "service_date": service_date.strftime("%Y-%m-%d"),
            "service_type": service_type,
            **ai_result
        }
    
    def generate_prior_auth(self, patient_id: str, service_type: str, diagnosis_codes: List[str], clinical_notes: str) -> Dict[str, Any]:
        """Generate prior authorization requirements."""
        # Get patient data
        patient = self.db.query(Patient).filter(Patient.insurance_id == patient_id).first()
        
        if not patient:
            return {"error": "Patient not found"}
        
        # Prepare clinical data
        clinical_data = {
            "patient_id": patient_id,
            "service_type": service_type,
            "diagnosis_codes": diagnosis_codes,
            "clinical_notes": clinical_notes,
            "patient_name": f"{patient.first_name} {patient.last_name}"
        }
        
        # Get AI analysis
        ai_result = ai_chains.prior_auth_chain(clinical_data)
        
        return {
            "patient": {
                "id": patient.insurance_id,
                "name": f"{patient.first_name} {patient.last_name}"
            },
            "service_type": service_type,
            "diagnosis_codes": diagnosis_codes,
            **ai_result
        }
    
    def suggest_coding(self, clinical_notes: str, service_type: str, provider_specialty: str) -> Dict[str, Any]:
        """Suggest medical coding based on clinical notes."""
        # Get AI analysis
        ai_result = ai_chains.coding_chain(clinical_notes, provider_specialty)
        
        return {
            "clinical_notes": clinical_notes,
            "service_type": service_type,
            "provider_specialty": provider_specialty,
            **ai_result
        }
    
    def scrub_claim(self, claim_data: Dict[str, Any], payer_rules: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Scrub claim for potential issues."""
        # Get AI analysis
        ai_result = ai_chains.scrubbing_chain(claim_data)
        
        return {
            "claim_data": claim_data,
            "payer_rules": payer_rules,
            **ai_result
        }
    
    def submit_claim(self, claim_data: Dict[str, Any], payer_id: str) -> Dict[str, Any]:
        """Submit claim to payer."""
        # Generate claim ID
        claim_id = f"CLM-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        
        # Mock submission process
        submission_status = "submitted"
        submission_date = datetime.now()
        
        # Create claim record
        claim = Claim(
            claim_id=claim_id,
            claim_date=datetime.now(),
            service_date=datetime.fromisoformat(claim_data.get("service_date", datetime.now().isoformat())),
            total_amount=float(claim_data.get("total_amount", 0)),
            status=ClaimStatus.SUBMITTED,
            submission_date=submission_date,
            patient_id=1,  # Mock patient ID
            provider_id=1,  # Mock provider ID
            payer_id=1,  # Mock payer ID
            encounter_id=1  # Mock encounter ID
        )
        
        self.db.add(claim)
        self.db.commit()
        
        return {
            "claim_id": claim_id,
            "status": submission_status,
            "submission_date": submission_date.isoformat(),
            "total_amount": claim_data.get("total_amount", 0)
        }
    
    def get_remittance(self, claim_id: str) -> Dict[str, Any]:
        """Get remittance information for claim."""
        # Mock remittance data
        remittance_data = {
            "claim_id": claim_id,
            "payment_date": datetime.now().isoformat(),
            "payment_amount": 1500.00,
            "adjustment_amount": 100.00,
            "payment_method": "EFT",
            "check_number": None,
            "payments": [
                {
                    "line_number": 1,
                    "cpt_code": "99213",
                    "paid_amount": 75.00,
                    "allowed_amount": 85.00,
                    "adjustment": 10.00
                }
            ],
            "adjustments": [
                {
                    "type": "Contractual",
                    "amount": 100.00,
                    "reason": "Contractual adjustment"
                }
            ]
        }
        
        return remittance_data
    
    def appeal_denial(self, denial_id: str, appeal_reason: str, additional_docs: Optional[List[str]] = None) -> Dict[str, Any]:
        """Appeal claim denial."""
        # Get denial data
        denial = self.db.query(Denial).filter(Denial.denial_id == denial_id).first()
        
        if not denial:
            return {"error": "Denial not found"}
        
        # Prepare denial data for AI analysis
        denial_data = {
            "denial_id": denial_id,
            "reason": denial.reason.value,
            "reason_description": denial.reason_description,
            "denial_date": denial.denial_date.isoformat(),
            "appeal_reason": appeal_reason
        }
        
        # Get AI analysis
        ai_result = ai_chains.denial_explainer_chain(denial_data)
        
        # Generate appeal ID
        appeal_id = f"APL-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        
        # Update denial status
        denial.appeal_status = "appealed"
        self.db.commit()
        
        return {
            "appeal_id": appeal_id,
            "denial_id": denial_id,
            "appeal_reason": appeal_reason,
            "additional_docs": additional_docs or [],
            **ai_result
        }
    
    def get_dashboard_stats(self, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Get dashboard statistics."""
        # For now, return mock statistics
        # In production, you would filter by user_id or organization
        stats = {
            "total_claims": 1250,
            "pending_claims": 45,
            "paid_claims": 1100,
            "denied_claims": 105,
            "total_revenue": 2500000.00,
            "avg_days_to_payment": 28,
            "denial_rate": 8.4,
            "clean_claim_rate": 91.6
        }
        
        return stats
