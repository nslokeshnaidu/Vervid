from agents.claim_extraction_agent import ClaimExtractionAgent
from agents.retrieval_agent import RetrievalAgent


claim_agent = ClaimExtractionAgent()
retrieval_agent = RetrievalAgent()


# Simulated video transcript
transcript = """
Hello everyone.

A nutritionally adequate diet is necessary for maintaining good health.
Carbohydrates are a major source of energy for the human body.

Thanks for watching.
"""


# -----------------------------------
# STEP 1: Extract factual claims
# -----------------------------------

claims = claim_agent.execute(transcript)

print("\n=== EXTRACTED CLAIMS ===")

for claim in claims:
    print("-", claim)


# -----------------------------------
# STEP 2: Retrieve evidence
# -----------------------------------

results = retrieval_agent.execute(claims)


print("\n=== RETRIEVED EVIDENCE ===")

for result in results:

    print("\n===================================")
    print("CLAIM:")
    print(result["claim"])

    print("\nLOCAL EVIDENCE:")

    for i, evidence in enumerate(
        result["local_evidence"],
        start=1
    ):
        print(f"\n--- Evidence {i} ---")
        print("Source:", evidence["source"])
        print("Distance:", evidence["distance"])
        print("Text:")
        print(evidence["text"])

    print("\nWEB EVIDENCE:")
    print(result["web_evidence"])