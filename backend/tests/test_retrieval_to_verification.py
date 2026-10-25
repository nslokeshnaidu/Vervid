from agents.retrieval_agent import RetrievalAgent
from agents.verification_agent import VerificationAgent


# --------------------------------------------------
# Create agents
# --------------------------------------------------

retrieval_agent = RetrievalAgent()
verification_agent = VerificationAgent()


# --------------------------------------------------
# Test claim
# --------------------------------------------------

claims = [
    "Higher waist circumference is associated with increased health risks."
]


# --------------------------------------------------
# STEP 1: Retrieve evidence from Local RAG
# --------------------------------------------------

print("\n==============================")
print("STEP 1: RETRIEVAL")
print("==============================")

retrieval_results = retrieval_agent.execute(claims)


# --------------------------------------------------
# STEP 2: Send REAL retrieved evidence
# to the Verification Agent
# --------------------------------------------------

print("\n==============================")
print("STEP 2: VERIFICATION")
print("==============================")


for result in retrieval_results:

    claim = result["claim"]

    evidence = result["local_evidence"]

    print("\nCLAIM:")
    print(claim)

    print("\nRetrieved evidence count:")
    print(len(evidence))

    print("\nSending retrieved evidence to Verification Agent...")

    verification_result = verification_agent.execute(
        claim=claim,
        evidence=evidence
    )

    print("\nVERIFICATION RESULT:")
    print(verification_result)