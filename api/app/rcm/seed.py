"""Data seeding for RCM platform."""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from flask import Flask, current_app
from app.core.db import get_db_session, init_db
import os
from dotenv import load_dotenv
from app.rcm.models import (
    Provider,
    Payer,
    Patient,
    Encounter,
    Claim,
    ClaimLine,
    Remittance,
    Denial,
    User,
    ClaimStatus,
    DenialReason,
)

load_dotenv("../../.env")


class RCMSeeder:
    """Seeder for RCM demo data."""

    def __init__(self, db: Session):
        """Initialize seeder with database session."""
        self.db = db

    def seed_providers(self) -> List[Provider]:
        """Seed provider data."""
        providers_data = [
            {
                "name": "Dr. Ahmed Al-Rashid",
                "npi": "1234567890",
                "specialty": "Cardiology",
                "address": "123 Healthcare Ave, Riyadh, Saudi Arabia",
                "phone": "+966-11-123-4567",
                "email": "ahmed.alrashid@healthcare.sa",
            },
            {
                "name": "Dr. Fatima Al-Zahra",
                "npi": "1234567891",
                "specialty": "Internal Medicine",
                "address": "456 Medical Center Blvd, Dubai, UAE",
                "phone": "+971-4-123-4567",
                "email": "fatima.alzahra@medical.ae",
            },
            {
                "name": "Dr. Omar Al-Hassan",
                "npi": "1234567892",
                "specialty": "Orthopedics",
                "address": "789 Hospital Street, Kuwait City, Kuwait",
                "phone": "+965-1-123-4567",
                "email": "omar.alhassan@hospital.kw",
            },
            {
                "name": "Dr. Layla Al-Mahmoud",
                "npi": "1234567893",
                "specialty": "Pediatrics",
                "address": "321 Clinic Road, Doha, Qatar",
                "phone": "+974-4-123-4567",
                "email": "layla.almahmoud@clinic.qa",
            },
            {
                "name": "Dr. Khalid Al-Sabah",
                "npi": "1234567894",
                "specialty": "Neurology",
                "address": "654 Medical Plaza, Muscat, Oman",
                "phone": "+968-2-123-4567",
                "email": "khalid.alsabah@medical.om",
            },
        ]

        providers = []
        for data in providers_data:
            provider = Provider(**data)
            self.db.add(provider)
            providers.append(provider)

        self.db.commit()
        return providers

    def seed_payers(self) -> List[Payer]:
        """Seed payer data."""
        payers_data = [
            {
                "name": "Ministry of Health - Saudi Arabia",
                "payer_id": "MOH-SA-001",
                "payer_type": "Government",
                "address": "Ministry of Health, Riyadh, Saudi Arabia",
                "phone": "+966-11-401-0000",
                "email": "claims@moh.gov.sa",
            },
            {
                "name": "Dubai Health Authority",
                "payer_id": "DHA-UAE-001",
                "payer_type": "Government",
                "address": "Dubai Health Authority, Dubai, UAE",
                "phone": "+971-4-219-0000",
                "email": "claims@dha.gov.ae",
            },
            {
                "name": "Kuwait Ministry of Health",
                "payer_id": "MOH-KW-001",
                "payer_type": "Government",
                "address": "Ministry of Health, Kuwait City, Kuwait",
                "phone": "+965-1-248-0000",
                "email": "claims@moh.gov.kw",
            },
            {
                "name": "Qatar Health Insurance Company",
                "payer_id": "QHIC-QA-001",
                "payer_type": "Private",
                "address": "Qatar Health Insurance, Doha, Qatar",
                "phone": "+974-4-499-0000",
                "email": "claims@qhic.qa",
            },
            {
                "name": "Oman Health Services",
                "payer_id": "OHS-OM-001",
                "payer_type": "Government",
                "address": "Oman Health Services, Muscat, Oman",
                "phone": "+968-2-419-0000",
                "email": "claims@ohs.gov.om",
            },
        ]

        payers = []
        for data in payers_data:
            payer = Payer(**data)
            self.db.add(payer)
            payers.append(payer)

        self.db.commit()
        return payers

    def seed_patients(self) -> List[Patient]:
        """Seed patient data."""
        patients_data = [
            {
                "first_name": "Abdullah",
                "last_name": "Al-Saud",
                "date_of_birth": datetime(1985, 3, 15),
                "gender": "Male",
                "address": "456 King Fahd Road, Riyadh, Saudi Arabia",
                "phone": "+966-50-123-4567",
                "email": "abdullah.alsaud@email.com",
                "insurance_id": "PAT-SA-001",
            },
            {
                "first_name": "Aisha",
                "last_name": "Al-Maktoum",
                "date_of_birth": datetime(1990, 7, 22),
                "gender": "Female",
                "address": "789 Sheikh Zayed Road, Dubai, UAE",
                "phone": "+971-50-123-4567",
                "email": "aisha.almaktoum@email.com",
                "insurance_id": "PAT-UAE-001",
            },
            {
                "first_name": "Mohammed",
                "last_name": "Al-Sabah",
                "date_of_birth": datetime(1978, 11, 8),
                "gender": "Male",
                "address": "321 Gulf Road, Kuwait City, Kuwait",
                "phone": "+965-50-123-4567",
                "email": "mohammed.alsabah@email.com",
                "insurance_id": "PAT-KW-001",
            },
            {
                "first_name": "Noor",
                "last_name": "Al-Thani",
                "date_of_birth": datetime(1992, 4, 12),
                "gender": "Female",
                "address": "654 Corniche Street, Doha, Qatar",
                "phone": "+974-50-123-4567",
                "email": "noor.althani@email.com",
                "insurance_id": "PAT-QA-001",
            },
            {
                "first_name": "Salim",
                "last_name": "Al-Busaidi",
                "date_of_birth": datetime(1983, 9, 30),
                "gender": "Male",
                "address": "987 Sultan Qaboos Street, Muscat, Oman",
                "phone": "+968-50-123-4567",
                "email": "salim.albusaidi@email.com",
                "insurance_id": "PAT-OM-001",
            },
        ]

        patients = []
        for data in patients_data:
            patient = Patient(**data)
            self.db.add(patient)
            patients.append(patient)

        self.db.commit()
        return patients

    def seed_encounters(
        self, providers: List[Provider], patients: List[Patient]
    ) -> List[Encounter]:
        """Seed encounter data."""
        encounter_types = ["Inpatient", "Outpatient", "Emergency", "Consultation"]
        diagnoses = ["E11.9", "I10", "E78.5", "Z51.11", "Z00.00"]
        procedures = ["99213", "99214", "99215", "99223", "99224"]

        encounters = []
        for i in range(20):
            encounter = Encounter(
                encounter_date=datetime.now() - timedelta(days=random.randint(1, 365)),
                encounter_type=random.choice(encounter_types),
                diagnosis_codes=json.dumps([random.choice(diagnoses)]),
                procedure_codes=json.dumps([random.choice(procedures)]),
                clinical_notes=f"Patient presented with {random.choice(['chest pain', 'diabetes', 'hypertension', 'routine checkup'])}",
                patient_id=random.choice(patients).id,
                provider_id=random.choice(providers).id,
            )
            self.db.add(encounter)
            encounters.append(encounter)

        self.db.commit()
        return encounters

    def seed_claims(
        self, encounters: List[Encounter], payers: List[Payer]
    ) -> List[Claim]:
        """Seed claim data."""
        claims = []
        for encounter in encounters:
            claim = Claim(
                claim_id=f"CLM-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}",
                claim_date=encounter.encounter_date + timedelta(days=1),
                service_date=encounter.encounter_date,
                total_amount=random.uniform(100.0, 2000.0),
                status=random.choice(list(ClaimStatus)),
                submission_date=encounter.encounter_date + timedelta(days=2),
                patient_id=encounter.patient_id,
                provider_id=encounter.provider_id,
                payer_id=random.choice(payers).id,
                encounter_id=encounter.id,
            )
            self.db.add(claim)
            claims.append(claim)

        self.db.commit()
        return claims

    def seed_claim_lines(self, claims: List[Claim]) -> List[ClaimLine]:
        """Seed claim line data."""
        cpt_codes = ["99213", "99214", "99215", "99223", "99224", "99232", "99233"]
        diagnoses = ["E11.9", "I10", "E78.5", "Z51.11", "Z00.00"]

        claim_lines = []
        for claim in claims:
            for line_num in range(1, random.randint(2, 4)):
                claim_line = ClaimLine(
                    line_number=line_num,
                    cpt_code=random.choice(cpt_codes),
                    diagnosis_codes=json.dumps([random.choice(diagnoses)]),
                    units=random.randint(1, 3),
                    unit_price=random.uniform(50.0, 500.0),
                    total_price=random.uniform(100.0, 1500.0),
                    description=f"Medical service line {line_num}",
                    claim_id=claim.id,
                )
                self.db.add(claim_line)
                claim_lines.append(claim_line)

        self.db.commit()
        return claim_lines

    def seed_remittances(
        self, claims: List[Claim], payers: List[Payer]
    ) -> List[Remittance]:
        """Seed remittance data."""
        remittances = []
        for claim in claims:
            if claim.status in [ClaimStatus.PAID, ClaimStatus.PROCESSING]:
                remittance = Remittance(
                    remittance_id=f"REM-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}",
                    payment_date=claim.submission_date
                    + timedelta(days=random.randint(15, 45)),
                    payment_amount=claim.total_amount * random.uniform(0.7, 0.95),
                    adjustment_amount=claim.total_amount * random.uniform(0.05, 0.3),
                    payment_method=random.choice(["EFT", "Check", "Wire Transfer"]),
                    check_number=f"CHK{random.randint(100000, 999999)}"
                    if random.choice([True, False])
                    else None,
                    claim_id=claim.id,
                    payer_id=claim.payer_id,
                )
                self.db.add(remittance)
                remittances.append(remittance)

        self.db.commit()
        return remittances

    def seed_denials(self, claims: List[Claim]) -> List[Denial]:
        """Seed denial data."""
        denials = []
        for claim in claims:
            if claim.status == ClaimStatus.DENIED:
                denial = Denial(
                    denial_id=f"DEN-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}",
                    denial_date=claim.submission_date
                    + timedelta(days=random.randint(10, 30)),
                    reason=random.choice(list(DenialReason)),
                    reason_description=random.choice(
                        [
                            "Missing clinical documentation",
                            "Invalid diagnosis codes",
                            "No prior authorization",
                            "Medical necessity not established",
                            "Duplicate claim submission",
                        ]
                    ),
                    appeal_deadline=datetime.now()
                    + timedelta(days=random.randint(30, 90)),
                    appeal_status="pending",
                    claim_id=claim.id,
                )
                self.db.add(denial)
                denials.append(denial)

        self.db.commit()
        return denials

    def seed_users(self) -> List[User]:
        """Seed user data."""
        users_data = [
            {"email": "admin@demo.com", "name": "Admin User", "role": "Admin"},
            {"email": "biller@demo.com", "name": "Biller User", "role": "Biller"},
            {"email": "coder@demo.com", "name": "Coder User", "role": "Coder"},
            {"email": "analyst@demo.com", "name": "Analyst User", "role": "Analyst"},
        ]

        users = []
        for data in users_data:
            user = User(**data)
            self.db.add(user)
            users.append(user)

        self.db.commit()
        return users

    def seed_all(self) -> Dict[str, Any]:
        """Seed all data."""
        print("Seeding providers...")
        providers = self.seed_providers()

        print("Seeding payers...")
        payers = self.seed_payers()

        print("Seeding patients...")
        patients = self.seed_patients()

        print("Seeding encounters...")
        encounters = self.seed_encounters(providers, patients)

        print("Seeding claims...")
        claims = self.seed_claims(encounters, payers)

        print("Seeding claim lines...")
        claim_lines = self.seed_claim_lines(claims)

        print("Seeding remittances...")
        remittances = self.seed_remittances(claims, payers)

        print("Seeding denials...")
        denials = self.seed_denials(claims)

        print("Seeding users...")
        users = self.seed_users()

        return {
            "providers": len(providers),
            "payers": len(payers),
            "patients": len(patients),
            "encounters": len(encounters),
            "claims": len(claims),
            "claim_lines": len(claim_lines),
            "remittances": len(remittances),
            "denials": len(denials),
            "users": len(users),
        }


def main():
    """Main seeding function."""
    try:
        app = current_app
        if not app:
            from flask import Flask

            app = Flask(__name__)
            app.config["DATABASE_URL"] = os.environ.get(
                "DATABASE_URL", "sqlite:///rcm_demo.db"
            )
    except RuntimeError:
        # Not in Flask app context, create one
        from flask import Flask

        app = Flask(__name__)
        app.config["DATABASE_URL"] = os.environ.get(
            "DATABASE_URL", "sqlite:///rcm_demo.db"
        )

    with app.app_context():
        init_db(app)
        db = get_db_session()
        seeder = RCMSeeder(db)

        try:
            result = seeder.seed_all()
            print(f"\nSeeding completed successfully!")
            print(f"Created: {result}")
        except Exception as e:
            print(f"Error during seeding: {e}")
            db.rollback()
        finally:
            db.close()


if __name__ == "__main__":
    main()
