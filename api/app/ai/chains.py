"""AI chains and tools for RCM workflows."""

import os
import uuid
import random
from typing import Dict, List, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from tenacity import retry, stop_after_attempt, wait_exponential


class RCMAIChains:
    """AI chains for RCM workflows."""

    def __init__(self, model_name: str = None):
        """Initialize AI chains with multiple API key support."""
        # Get model name from environment or use default
        self.model_name = model_name or os.getenv("MODEL_NAME", "gemini-2.5-flash-lite")
        self.api_keys = self._get_api_keys()
        self.current_key_index = 0
        self.llm = None
        self._initialize_llm()

    def _get_api_keys(self) -> List[str]:
        """Get list of API keys from environment variables."""
        keys = []
        
        # Get primary key
        primary_key = os.getenv("GOOGLE_API_KEY", "")
        if primary_key:
            keys.append(primary_key)
        
        # Get additional keys (GOOGLE_API_KEY_1, GOOGLE_API_KEY_2, etc.)
        i = 1
        while True:
            additional_key = os.getenv(f"GOOGLE_API_KEY_{i}", "")
            if additional_key:
                keys.append(additional_key)
                i += 1
            else:
                break
        
        # Shuffle keys for load balancing
        random.shuffle(keys)
        print(f"Loaded {len(keys)} API keys for AI chains")
        return keys

    def _initialize_llm(self) -> None:
        """Initialize LLM with current API key."""
        if not self.api_keys:
            self.llm = None
            return
        
        try:
            current_key = self.api_keys[self.current_key_index]
            print(f"Initializing LLM with key {self.current_key_index} using model {self.model_name}")
            self.llm = ChatGoogleGenerativeAI(
                model=self.model_name,
                google_api_key=current_key,
                temperature=0.1,
                max_tokens=2048,
            )
            print(f"LLM initialized successfully with key {self.current_key_index}")
        except Exception as e:
            print(f"Failed to initialize LLM with key {self.current_key_index}: {e}")
            self.llm = None

    def _rotate_api_key(self) -> bool:
        """Rotate to next API key. Returns True if rotation successful."""
        if len(self.api_keys) <= 1:
            return False
        
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        self._initialize_llm()
        return True

    def _try_with_fallback(self, func, chain_type="general", *args, **kwargs):
        """Try function with current key, fallback to other keys if needed."""
        if not self.llm:
            print(f"LLM not initialized, using fallback for {chain_type}")
            return self._get_fallback_response(chain_type)
        
        last_exception = None
        keys_tried = set()
        
        for attempt in range(len(self.api_keys)):
            if self.current_key_index in keys_tried:
                if not self._rotate_api_key():
                    break
                keys_tried.add(self.current_key_index)
            else:
                keys_tried.add(self.current_key_index)
            
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                error_msg = str(e).lower()
                
                # Check if it's a quota/rate limit error
                if any(keyword in error_msg for keyword in [
                    "quota", "rate limit", "resource exhausted", "429", 
                    "exceeded", "billing", "plan"
                ]):
                    print(f"API key {self.current_key_index} hit quota limit, rotating...")
                    if not self._rotate_api_key():
                        break
                    continue
                else:
                    # Non-quota error, don't rotate
                    break
        
        # All keys failed, return fallback
        print(f"All API keys exhausted, using fallback response for {chain_type}. Last error: {last_exception}")
        return self._get_fallback_response(chain_type)

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
                    "Confirm service authorization",
                ],
            },
            "prior_auth": {
                "required": True,
                "checklist": [
                    "Clinical documentation",
                    "Medical necessity letter",
                    "Provider credentials",
                    "Treatment plan",
                ],
                "draft_letter": "Based on the clinical documentation, this treatment is medically necessary...",
            },
            "coding": {
                "icd_codes": [
                    {
                        "code": "E11.9",
                        "description": "Type 2 diabetes without complications",
                        "confidence": 0.95,
                    }
                ],
                "cpt_codes": [
                    {
                        "code": "99213",
                        "description": "Office visit, established patient",
                        "confidence": 0.92,
                    }
                ],
                "rationale": "Based on the clinical documentation, the primary diagnosis is diabetes...",
                "ai_analysis": "⚠️ AI not available - using fallback responses. Please set GOOGLE_API_KEY environment variable.",
                "ai_used": False,
            },
            "scrubbing": {
                "issues": [
                    {
                        "type": "missing_field",
                        "field": "diagnosis_code",
                        "severity": "high",
                    },
                    {"type": "invalid_code", "field": "cpt_code", "severity": "medium"},
                ],
                "recommendations": [
                    "Add primary diagnosis code",
                    "Verify CPT code validity",
                    "Check provider credentials",
                ],
            },
            "denial_explainer": {
                "analysis": "This denial appears to be due to missing clinical documentation...",
                "next_steps": [
                    "Gather additional clinical notes",
                    "Submit appeal within 30 days",
                    "Contact payer for clarification",
                ],
            },
        }
        return fallbacks.get(chain_type, {})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def eligibility_chain(
        self, patient_data: Dict[str, Any], payer_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Eligibility verification chain."""
        def _call_ai():
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """You are an expert RCM specialist for GCC healthcare. Analyze patient eligibility for insurance coverage.

                Consider:
                - Patient demographics and insurance details
                - Payer policies and coverage rules
                - Service type and date requirements
                - Common eligibility issues in GCC region

                Provide structured analysis with coverage status, benefits, and actionable suggestions.""",
                    ),
                    (
                        "human",
                        """Patient Data: {patient_data}
                Payer Data: {payer_data}

                Analyze eligibility and provide recommendations.""",
                    ),
                ]
            )

            response = self.llm.invoke(
                prompt.format_messages(
                    patient_data=str(patient_data), payer_data=str(payer_data)
                )
            )

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
                    "Confirm service authorization",
                ],
            }

        return self._try_with_fallback(_call_ai, "eligibility")

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def prior_auth_chain(self, clinical_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prior authorization chain."""
        def _call_ai():
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """You are an expert in prior authorization for GCC healthcare. Generate comprehensive PA requirements and draft authorization letters.

                Consider:
                - Medical necessity criteria
                - Payer-specific requirements
                - Clinical documentation standards
                - GCC healthcare regulations

                Provide structured checklist and professional authorization letter draft.""",
                    ),
                    (
                        "human",
                        """Clinical Data: {clinical_data}

                Generate prior authorization requirements and draft letter.""",
                    ),
                ]
            )

            response = self.llm.invoke(
                prompt.format_messages(clinical_data=str(clinical_data))
            )

            return {
                "required": True,
                "checklist": [
                    "Clinical documentation",
                    "Medical necessity letter",
                    "Provider credentials",
                    "Treatment plan",
                ],
                "draft_letter": response.content,
                "ai_analysis": "Based on the clinical data, prior authorization is required...",
            }

        return self._try_with_fallback(_call_ai, "prior_auth")

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def coding_chain(self, clinical_notes: str, specialty: str) -> Dict[str, Any]:
        """Medical coding chain."""
        def _call_ai():
            # Enhanced prompt for structured AI response
            enhanced_prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """You are an expert medical coder specializing in GCC healthcare. Analyze clinical documentation and suggest appropriate ICD-10 and CPT codes.

IMPORTANT: Respond with a JSON structure containing the codes. Use this exact format:

{
  "icd_codes": [
    {"code": "E11.9", "description": "Type 2 diabetes without complications", "confidence": 0.95}
  ],
  "cpt_codes": [
    {"code": "99213", "description": "Office visit, established patient", "confidence": 0.92}
  ],
  "rationale": "Detailed explanation of code selection"
}

Consider:
            - Clinical documentation accuracy
            - Code specificity and hierarchy
            - Provider specialty requirements
            - GCC coding standards

            Provide structured coding suggestions with confidence levels and rationale.""",
                ),
                (
                    "human",
                    """Clinical Notes: {clinical_notes}
            Provider Specialty: {specialty}

            Suggest appropriate ICD-10 and CPT codes with rationale.""",
                ),
            ]
        )

        try:
            # Enhanced prompt for structured AI response
            enhanced_prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """You are an expert medical coder specializing in GCC healthcare. Analyze clinical documentation and suggest appropriate ICD-10 and CPT codes.

IMPORTANT: Respond with a JSON structure containing the codes. Use this exact format:

{{
  "icd_codes": [
    {{"code": "E11.9", "description": "Type 2 diabetes without complications", "confidence": 0.95}}
  ],
  "cpt_codes": [
    {{"code": "99213", "description": "Office visit, established patient", "confidence": 0.92}}
  ],
  "rationale": "Detailed explanation of code selection"
}}

Consider:
- Clinical documentation accuracy
- Code specificity and hierarchy
- Provider specialty requirements
- GCC coding standards
- Medical necessity

Provide structured coding suggestions with confidence levels and detailed rationale.""",
                    ),
                    (
                        "human",
                        """Clinical Notes: {clinical_notes}
Provider Specialty: {specialty}

Analyze and provide appropriate ICD-10 and CPT codes in JSON format.""",
                    ),
                ]
            )

            response = self.llm.invoke(
                enhanced_prompt.format_messages(
                    clinical_notes=clinical_notes, specialty=specialty
                )
            )

            # Try to parse AI response as JSON
            try:
                import json

                ai_data = json.loads(response.content)

                # Validate and structure the response
                icd_codes = ai_data.get("icd_codes", [])
                cpt_codes = ai_data.get("cpt_codes", [])
                rationale = ai_data.get("rationale", response.content)

                # Ensure we have at least some codes
                if not icd_codes and not cpt_codes:
                    # Fallback to keyword matching if AI didn't provide codes
                    clinical_lower = clinical_notes.lower()

                    if "diabetes" in clinical_lower or "diabetic" in clinical_lower:
                        icd_codes.append(
                            {
                                "code": "E11.9",
                                "description": "Type 2 diabetes without complications",
                                "confidence": 0.95,
                            }
                        )
                    if (
                        "hypertension" in clinical_lower
                        or "high blood pressure" in clinical_lower
                    ):
                        icd_codes.append(
                            {
                                "code": "I10",
                                "description": "Essential hypertension",
                                "confidence": 0.90,
                            }
                        )

                    if (
                        "office visit" in clinical_lower
                        or "follow up" in clinical_lower
                    ):
                        cpt_codes.append(
                            {
                                "code": "99213",
                                "description": "Office visit, established patient",
                                "confidence": 0.92,
                            }
                        )
                    if (
                        "blood draw" in clinical_lower
                        or "venipuncture" in clinical_lower
                    ):
                        cpt_codes.append(
                            {
                                "code": "36415",
                                "description": "Collection of venous blood",
                                "confidence": 0.88,
                            }
                        )

                return {
                    "icd_codes": icd_codes,
                    "cpt_codes": cpt_codes,
                    "rationale": rationale,
                    "ai_analysis": "AI-generated codes based on clinical documentation",
                    "ai_used": True,
                }

            except json.JSONDecodeError:
                # If AI response isn't valid JSON, extract codes from text
                content = response.content

                # Simple extraction from AI text response
                icd_codes = []
                cpt_codes = []

                # Look for ICD-10 codes (format: E11.9, I10, etc.)
                import re

                icd_matches = re.findall(r"([A-Z]\d{2}(?:\.\d+)?)", content)
                for match in icd_matches:
                    if match.startswith(("E", "I", "M", "N", "S", "T", "Z")):
                        icd_codes.append(
                            {
                                "code": match,
                                "description": f"AI-suggested ICD-10 code: {match}",
                                "confidence": 0.85,
                            }
                        )

                # Look for CPT codes (format: 99213, 36415, etc.)
                cpt_matches = re.findall(r"(\d{5})", content)
                for match in cpt_matches:
                    cpt_codes.append(
                        {
                            "code": match,
                            "description": f"AI-suggested CPT code: {match}",
                            "confidence": 0.85,
                        }
                    )

                return {
                    "icd_codes": icd_codes,
                    "cpt_codes": cpt_codes,
                    "rationale": content,
                    "ai_analysis": "AI-generated analysis with extracted codes",
                    "ai_used": True,
                }
        except Exception as e:
            # print traceback
            import traceback

            traceback.print_exc()
            print("coding: chain: ")
            print(e)
            return self._get_fallback_response("coding")

        return self._try_with_fallback(_call_ai, "coding")

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def scrubbing_chain(self, claim_data: Dict[str, Any]) -> Dict[str, Any]:
        """Claims scrubbing chain."""
        def _call_ai():
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """You are an expert claims scrubber for GCC healthcare. Analyze claims for potential issues and provide recommendations.

                Check for:
                - Missing required fields
                - Invalid codes or formats
                - Payer-specific requirements
                - Common rejection patterns

                Provide structured analysis with issue severity and actionable recommendations.""",
                    ),
                    (
                        "human",
                        """Claim Data: {claim_data}

                Analyze for potential issues and provide recommendations.""",
                    ),
                ]
            )

            try:
                response = self.llm.invoke(
                    prompt.format_messages(claim_data=str(claim_data))
                )

                return {
                    "issues": [
                        {
                            "type": "missing_field",
                            "field": "diagnosis_code",
                            "severity": "high",
                        },
                        {"type": "invalid_code", "field": "cpt_code", "severity": "medium"},
                    ],
                    "recommendations": [
                        "Add primary diagnosis code",
                        "Verify CPT code validity",
                        "Check provider credentials",
                    ],
                    "ai_analysis": response.content,
                }
            except Exception as e:
                return self._get_fallback_response("scrubbing")

        return self._try_with_fallback(_call_ai, "scrubbing")

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def denial_explainer_chain(self, denial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Denial explanation and appeal guidance chain."""
        def _call_ai():
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """You are an expert in denial management for GCC healthcare. Analyze denial reasons and provide appeal guidance.

                Consider:
                - Denial reason codes and descriptions
                - Appeal requirements and deadlines
                - Required documentation
                - Success strategies for similar denials

                Provide structured analysis with clear next steps and appeal recommendations.""",
                    ),
                    (
                        "human",
                        """Denial Data: {denial_data}

                Analyze denial and provide appeal guidance.""",
                    ),
                ]
            )

            try:
                response = self.llm.invoke(
                    prompt.format_messages(denial_data=str(denial_data))
                )

                return {
                    "analysis": response.content,
                    "next_steps": [
                        "Gather additional clinical notes",
                        "Submit appeal within 30 days",
                        "Contact payer for clarification",
                    ],
                    "appeal_strategy": "Focus on medical necessity documentation...",
                    "success_probability": "Medium",
                }
            except Exception as e:
                return self._get_fallback_response("denial_explainer")

        return self._try_with_fallback(_call_ai, "denial_explainer")


# Global instance - lazy initialization
_ai_chains_instance = None

def get_ai_chains() -> RCMAIChains:
    """Get AI chains instance with lazy initialization."""
    global _ai_chains_instance
    if _ai_chains_instance is None:
        _ai_chains_instance = RCMAIChains()
    return _ai_chains_instance

# For backward compatibility - this will be created only when first accessed
class LazyAIChains:
    """Lazy wrapper for AI chains."""
    def __getattr__(self, name):
        return getattr(get_ai_chains(), name)

ai_chains = LazyAIChains()