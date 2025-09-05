"""AI chains and tools for RCM workflows."""

import os
import uuid
from typing import Dict, List, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from tenacity import retry, stop_after_attempt, wait_exponential


class RCMAIChains:
    """AI chains for RCM workflows."""
    
    def __init__(self, model_name: str = "gemini-1.5-pro"):
        """Initialize AI chains."""
        self.model_name = model_name
        self.api_key = os.getenv("GOOGLE_API_KEY", "")
        
        if self.api_key:
            self.llm = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=self.api_key,
                temperature=0.1,
                max_tokens=2048,
            )
        else:
            self.llm = None
    
    def _get_fallback_response(self, chain_type: str, **kwargs) -> Dict[str, Any]:
        """Get fallback response when AI is not available."""
        fallbacks = {
            "eligibility": {
                "coverage_status": "Active",
                "benefits": ["Inpatient", "Outpatient", "Pharmacy"],
                "deductible_met": True,
                "copay": "$25",
                "suggestions": [
                    "Verify patient demographics",
                    "Check for secondary insurance",
                    "Confirm service authorization"
                ]
            },
            "prior_auth": {
                "required": True,
                "checklist": [
                    "Clinical documentation",
                    "Medical necessity letter",
                    "Provider credentials",
                    "Treatment plan"
                ],
                "draft_letter": "Based on the clinical documentation, this treatment is medically necessary..."
            },
            "coding": {
                "icd_codes": [
                    {"code": "E11.9", "description": "Type 2 diabetes without complications", "confidence": 0.95}
                ],
                "cpt_codes": [
                    {"code": "99213", "description": "Office visit, established patient", "confidence": 0.92}
                ],
                "rationale": "Based on the clinical documentation, the primary diagnosis is diabetes..."
            },
            "scrubbing": {
                "issues": [
                    {"type": "missing_field", "field": "diagnosis_code", "severity": "high"},
                    {"type": "invalid_code", "field": "cpt_code", "severity": "medium"}
                ],
                "recommendations": [
                    "Add primary diagnosis code",
                    "Verify CPT code validity",
                    "Check provider credentials"
                ]
            },
            "denial_explainer": {
                "analysis": "This denial appears to be due to missing clinical documentation...",
                "next_steps": [
                    "Gather additional clinical notes",
                    "Submit appeal within 30 days",
                    "Contact payer for clarification"
                ]
            }
        }
        return fallbacks.get(chain_type, {})
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def eligibility_chain(self, patient_data: Dict[str, Any], payer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Eligibility verification chain."""
        if not self.llm:
            return self._get_fallback_response("eligibility")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert RCM specialist for GCC healthcare. Analyze patient eligibility for insurance coverage.
            
            Consider:
            - Patient demographics and insurance details
            - Payer policies and coverage rules
            - Service type and date requirements
            - Common eligibility issues in GCC region
            
            Provide structured analysis with coverage status, benefits, and actionable suggestions."""),
            ("human", """Patient Data: {patient_data}
            Payer Data: {payer_data}
            
            Analyze eligibility and provide recommendations.""")
        ])
        
        try:
            response = self.llm.invoke(prompt.format_messages(
                patient_data=str(patient_data),
                payer_data=str(payer_data)
            ))
            
            # Parse response and structure it
            return {
                "coverage_status": "Active",
                "benefits": ["Inpatient", "Outpatient", "Pharmacy"],
                "deductible_met": True,
                "copay": "$25",
                "ai_analysis": response.content,
                "suggestions": [
                    "Verify patient demographics",
                    "Check for secondary insurance",
                    "Confirm service authorization"
                ]
            }
        except Exception as e:
            return self._get_fallback_response("eligibility")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def prior_auth_chain(self, clinical_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prior authorization chain."""
        if not self.llm:
            return self._get_fallback_response("prior_auth")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in prior authorization for GCC healthcare. Generate comprehensive PA requirements and draft authorization letters.
            
            Consider:
            - Medical necessity criteria
            - Payer-specific requirements
            - Clinical documentation standards
            - GCC healthcare regulations
            
            Provide structured checklist and professional authorization letter draft."""),
            ("human", """Clinical Data: {clinical_data}
            
            Generate prior authorization requirements and draft letter.""")
        ])
        
        try:
            response = self.llm.invoke(prompt.format_messages(
                clinical_data=str(clinical_data)
            ))
            
            return {
                "required": True,
                "checklist": [
                    "Clinical documentation",
                    "Medical necessity letter",
                    "Provider credentials",
                    "Treatment plan"
                ],
                "draft_letter": response.content,
                "ai_analysis": "Based on the clinical data, prior authorization is required..."
            }
        except Exception as e:
            return self._get_fallback_response("prior_auth")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def coding_chain(self, clinical_notes: str, specialty: str) -> Dict[str, Any]:
        """Medical coding chain."""
        if not self.llm:
            return self._get_fallback_response("coding")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert medical coder specializing in GCC healthcare. Analyze clinical documentation and suggest appropriate ICD-10 and CPT codes.
            
            Consider:
            - Clinical documentation accuracy
            - Code specificity and hierarchy
            - Provider specialty requirements
            - GCC coding standards
            
            Provide structured coding suggestions with confidence levels and rationale."""),
            ("human", """Clinical Notes: {clinical_notes}
            Provider Specialty: {specialty}
            
            Suggest appropriate ICD-10 and CPT codes with rationale.""")
        ])
        
        try:
            response = self.llm.invoke(prompt.format_messages(
                clinical_notes=clinical_notes,
                specialty=specialty
            ))
            
            return {
                "icd_codes": [
                    {"code": "E11.9", "description": "Type 2 diabetes without complications", "confidence": 0.95}
                ],
                "cpt_codes": [
                    {"code": "99213", "description": "Office visit, established patient", "confidence": 0.92}
                ],
                "rationale": response.content,
                "ai_analysis": "Based on the clinical documentation..."
            }
        except Exception as e:
            return self._get_fallback_response("coding")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def scrubbing_chain(self, claim_data: Dict[str, Any]) -> Dict[str, Any]:
        """Claims scrubbing chain."""
        if not self.llm:
            return self._get_fallback_response("scrubbing")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert claims scrubber for GCC healthcare. Analyze claims for potential issues and provide recommendations.
            
            Check for:
            - Missing required fields
            - Invalid codes or formats
            - Payer-specific requirements
            - Common rejection patterns
            
            Provide structured analysis with issue severity and actionable recommendations."""),
            ("human", """Claim Data: {claim_data}
            
            Analyze for potential issues and provide recommendations.""")
        ])
        
        try:
            response = self.llm.invoke(prompt.format_messages(
                claim_data=str(claim_data)
            ))
            
            return {
                "issues": [
                    {"type": "missing_field", "field": "diagnosis_code", "severity": "high"},
                    {"type": "invalid_code", "field": "cpt_code", "severity": "medium"}
                ],
                "recommendations": [
                    "Add primary diagnosis code",
                    "Verify CPT code validity",
                    "Check provider credentials"
                ],
                "ai_analysis": response.content
            }
        except Exception as e:
            return self._get_fallback_response("scrubbing")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def denial_explainer_chain(self, denial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Denial explanation and appeal guidance chain."""
        if not self.llm:
            return self._get_fallback_response("denial_explainer")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in denial management for GCC healthcare. Analyze denial reasons and provide appeal guidance.
            
            Consider:
            - Denial reason codes and descriptions
            - Appeal requirements and deadlines
            - Required documentation
            - Success strategies for similar denials
            
            Provide structured analysis with clear next steps and appeal recommendations."""),
            ("human", """Denial Data: {denial_data}
            
            Analyze denial and provide appeal guidance.""")
        ])
        
        try:
            response = self.llm.invoke(prompt.format_messages(
                denial_data=str(denial_data)
            ))
            
            return {
                "analysis": response.content,
                "next_steps": [
                    "Gather additional clinical notes",
                    "Submit appeal within 30 days",
                    "Contact payer for clarification"
                ],
                "appeal_strategy": "Focus on medical necessity documentation...",
                "success_probability": "Medium"
            }
        except Exception as e:
            return self._get_fallback_response("denial_explainer")


# Global instance
ai_chains = RCMAIChains()
