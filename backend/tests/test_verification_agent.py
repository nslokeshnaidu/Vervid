from agents.verification_agent import VerificationAgent


agent = VerificationAgent()


# ==================================================
# TEST 1 — SUPPORTED
# ==================================================

claim_1 = "Higher waist circumference is associated with increased health risks."

evidence_1 = [
    {
        "source": "DietaryGuidelinesforNINwebsite.pdf",
        "distance": 0.72,
        "text": (
            "Waist circumference 90cm for men and 80cm for women "
            "are associated with increased risk of several chronic "
            "diseases especially in Asian Indians."
        )
    }
]


# ==================================================
# TEST 2 — CONTRADICTED
# ==================================================

claim_2 = "Higher waist circumference has no association with health risks."

evidence_2 = [
    {
        "source": "DietaryGuidelinesforNINwebsite.pdf",
        "distance": 0.70,
        "text": (
            "Waist circumference 90cm for men and 80cm for women "
            "are associated with increased risk of several chronic "
            "diseases especially in Asian Indians."
        )
    }
]


# ==================================================
# TEST 3 — INSUFFICIENT
# ==================================================

claim_3 = "Eating bananas prevents obesity."

evidence_3 = [
    {
        "source": "DietaryGuidelinesforNINwebsite.pdf",
        "distance": 0.90,
        "text": (
            "Carbohydrates are major sources of energy in the human diet."
        )
    }
]


# ==================================================
# RUN TESTS
# ==================================================

tests = [
    ("SUPPORTED TEST", claim_1, evidence_1),
    ("CONTRADICTED TEST", claim_2, evidence_2),
    ("INSUFFICIENT TEST", claim_3, evidence_3),
]


for test_name, claim, evidence in tests:

    print("\n")
    print("=" * 60)
    print(test_name)
    print("=" * 60)

    print("\nCLAIM:")
    print(claim)

    result = agent.execute(
        claim=claim,
        evidence=evidence
    )

    print("\nVERIFICATION RESULT:")
    print(result)