"""Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    """Base response model."""
    success: bool = True
    message: str = "Success"
    trace_id: Optional[str] = None


class ErrorResponse(BaseResponse):
    """Error response model."""
    success: bool = False
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


# Eligibility Schemas
class EligibilityRequest(BaseModel):
    """Eligibility check request."""
    patient_id: str = Field(..., description="Patient identifier")
    payer_id: str = Field(..., description="Payer identifier")
    service_date: datetime = Field(..., description="Service date")
    service_type: str = Field(..., description="Type of service")


class EligibilityResponse(BaseResponse):
    """Eligibility check response."""
    data: Dict[str, Any] = Field(..., description="Eligibility information")
    ai_suggestions: List[str] = Field(default_factory=list, description="AI suggestions")


# Prior Auth Schemas
class PriorAuthRequest(BaseModel):
    """Prior authorization request."""
    patient_id: str = Field(..., description="Patient identifier")
    service_type: str = Field(..., description="Service type")
    diagnosis_codes: List[str] = Field(..., description="Diagnosis codes")
    clinical_notes: str = Field(..., description="Clinical notes")


class PriorAuthResponse(BaseResponse):
    """Prior authorization response."""
    data: Dict[str, Any] = Field(..., description="Prior auth information")
    checklist: List[str] = Field(default_factory=list, description="Required checklist")
    draft_letter: Optional[str] = Field(None, description="Draft authorization letter")


# Coding Schemas
class CodingRequest(BaseModel):
    """Medical coding request."""
    clinical_notes: str = Field(..., description="Clinical documentation")
    service_type: str = Field(..., description="Service type")
    provider_specialty: str = Field(..., description="Provider specialty")


class CodingResponse(BaseResponse):
    """Medical coding response."""
    data: Dict[str, Any] = Field(..., description="Coding suggestions")
    icd_codes: List[Dict[str, Any]] = Field(default_factory=list, description="ICD-10 codes")
    cpt_codes: List[Dict[str, Any]] = Field(default_factory=list, description="CPT codes")
    rationale: str = Field(..., description="Coding rationale")


# Scrubbing Schemas
class ScrubbingRequest(BaseModel):
    """Claims scrubbing request."""
    claim_data: Dict[str, Any] = Field(..., description="Claim information")
    payer_rules: Optional[Dict[str, Any]] = Field(None, description="Payer-specific rules")


class ScrubbingResponse(BaseResponse):
    """Claims scrubbing response."""
    data: Dict[str, Any] = Field(..., description="Scrubbing results")
    issues: List[Dict[str, Any]] = Field(default_factory=list, description="Identified issues")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")


# Claims Submission Schemas
class ClaimsSubmissionRequest(BaseModel):
    """Claims submission request."""
    claim_data: Dict[str, Any] = Field(..., description="Complete claim data")
    payer_id: str = Field(..., description="Target payer")


class ClaimsSubmissionResponse(BaseResponse):
    """Claims submission response."""
    data: Dict[str, Any] = Field(..., description="Submission results")
    claim_id: str = Field(..., description="Generated claim ID")
    status: str = Field(..., description="Submission status")


# Remittance Schemas
class RemittanceResponse(BaseResponse):
    """Remittance tracking response."""
    data: Dict[str, Any] = Field(..., description="Remittance information")
    payments: List[Dict[str, Any]] = Field(default_factory=list, description="Payment details")
    adjustments: List[Dict[str, Any]] = Field(default_factory=list, description="Adjustments")


# Denial Management Schemas
class DenialAppealRequest(BaseModel):
    """Denial appeal request."""
    denial_id: str = Field(..., description="Denial identifier")
    appeal_reason: str = Field(..., description="Appeal reasoning")
    additional_docs: Optional[List[str]] = Field(None, description="Additional documentation")


class DenialAppealResponse(BaseResponse):
    """Denial appeal response."""
    data: Dict[str, Any] = Field(..., description="Appeal information")
    appeal_id: str = Field(..., description="Generated appeal ID")
    next_steps: List[str] = Field(default_factory=list, description="Next steps")
    ai_analysis: Optional[str] = Field(None, description="AI analysis of denial")
