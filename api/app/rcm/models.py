"""SQLAlchemy models for RCM entities."""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

from app.core.db import Base


class ClaimStatus(enum.Enum):
    """Claim status enumeration."""
    DRAFT = "draft"
    PENDING = "pending"
    SUBMITTED = "submitted"
    PROCESSING = "processing"
    PAID = "paid"
    DENIED = "denied"
    APPEALED = "appealed"
    CLOSED = "closed"


class DenialReason(enum.Enum):
    """Denial reason enumeration."""
    MISSING_INFO = "missing_information"
    INVALID_CODES = "invalid_codes"
    NO_AUTHORIZATION = "no_authorization"
    MEDICAL_NECESSITY = "medical_necessity"
    DUPLICATE = "duplicate_claim"
    TIMELY_FILING = "timely_filing"
    OTHER = "other"


class TimestampMixin:
    """Mixin for timestamp fields."""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Provider(Base, TimestampMixin):
    """Provider model."""
    __tablename__ = "providers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    npi = Column(String(10), unique=True, nullable=False)
    specialty = Column(String(100), nullable=False)
    address = Column(Text, nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    encounters = relationship("Encounter", back_populates="provider")
    claims = relationship("Claim", back_populates="provider")


class Payer(Base, TimestampMixin):
    """Payer model."""
    __tablename__ = "payers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    payer_id = Column(String(50), unique=True, nullable=False)
    payer_type = Column(String(50), nullable=False)  # Government, Private, etc.
    address = Column(Text, nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    claims = relationship("Claim", back_populates="payer")
    remittances = relationship("Remittance", back_populates="payer")


class Patient(Base, TimestampMixin):
    """Patient model."""
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    gender = Column(String(10), nullable=False)
    address = Column(Text, nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=True)
    insurance_id = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    encounters = relationship("Encounter", back_populates="patient")
    claims = relationship("Claim", back_populates="patient")


class Encounter(Base, TimestampMixin):
    """Encounter model."""
    __tablename__ = "encounters"
    
    id = Column(Integer, primary_key=True, index=True)
    encounter_date = Column(DateTime, nullable=False)
    encounter_type = Column(String(50), nullable=False)  # Inpatient, Outpatient, etc.
    diagnosis_codes = Column(Text, nullable=True)  # JSON string
    procedure_codes = Column(Text, nullable=True)  # JSON string
    clinical_notes = Column(Text, nullable=True)
    
    # Foreign keys
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False)
    
    # Relationships
    patient = relationship("Patient", back_populates="encounters")
    provider = relationship("Provider", back_populates="encounters")
    claims = relationship("Claim", back_populates="encounter")


class Claim(Base, TimestampMixin):
    """Claim model."""
    __tablename__ = "claims"
    
    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(String(50), unique=True, nullable=False)
    claim_date = Column(DateTime, nullable=False)
    service_date = Column(DateTime, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(ClaimStatus), default=ClaimStatus.DRAFT, nullable=False)
    submission_date = Column(DateTime, nullable=True)
    
    # Foreign keys
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False)
    payer_id = Column(Integer, ForeignKey("payers.id"), nullable=False)
    encounter_id = Column(Integer, ForeignKey("encounters.id"), nullable=False)
    
    # Relationships
    patient = relationship("Patient", back_populates="claims")
    provider = relationship("Provider", back_populates="claims")
    payer = relationship("Payer", back_populates="claims")
    encounter = relationship("Encounter", back_populates="claims")
    claim_lines = relationship("ClaimLine", back_populates="claim")
    remittances = relationship("Remittance", back_populates="claim")
    denials = relationship("Denial", back_populates="claim")


class ClaimLine(Base, TimestampMixin):
    """Claim line model."""
    __tablename__ = "claim_lines"
    
    id = Column(Integer, primary_key=True, index=True)
    line_number = Column(Integer, nullable=False)
    cpt_code = Column(String(10), nullable=False)
    diagnosis_codes = Column(Text, nullable=False)  # JSON string
    units = Column(Integer, default=1, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    
    # Foreign keys
    claim_id = Column(Integer, ForeignKey("claims.id"), nullable=False)
    
    # Relationships
    claim = relationship("Claim", back_populates="claim_lines")


class Remittance(Base, TimestampMixin):
    """Remittance model."""
    __tablename__ = "remittances"
    
    id = Column(Integer, primary_key=True, index=True)
    remittance_id = Column(String(50), unique=True, nullable=False)
    payment_date = Column(DateTime, nullable=False)
    payment_amount = Column(Float, nullable=False)
    adjustment_amount = Column(Float, default=0.0, nullable=False)
    payment_method = Column(String(50), nullable=False)
    check_number = Column(String(50), nullable=True)
    
    # Foreign keys
    claim_id = Column(Integer, ForeignKey("claims.id"), nullable=False)
    payer_id = Column(Integer, ForeignKey("payers.id"), nullable=False)
    
    # Relationships
    claim = relationship("Claim", back_populates="remittances")
    payer = relationship("Payer", back_populates="remittances")


class Denial(Base, TimestampMixin):
    """Denial model."""
    __tablename__ = "denials"
    
    id = Column(Integer, primary_key=True, index=True)
    denial_id = Column(String(50), unique=True, nullable=False)
    denial_date = Column(DateTime, nullable=False)
    reason = Column(Enum(DenialReason), nullable=False)
    reason_description = Column(Text, nullable=False)
    appeal_deadline = Column(DateTime, nullable=True)
    appeal_status = Column(String(50), default="pending", nullable=False)
    
    # Foreign keys
    claim_id = Column(Integer, ForeignKey("claims.id"), nullable=False)
    
    # Relationships
    claim = relationship("Claim", back_populates="denials")


class User(Base, TimestampMixin):
    """User model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)  # Admin, Biller, Coder, Analyst
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, nullable=True)
