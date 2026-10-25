from agents.retrieval_agent import RetrievalAgent


# Create the Retrieval Agent
retrieval_agent = RetrievalAgent()


# Simulate claims coming from ClaimExtractionAgent
claims = [
    "Nutritionally adequate food is necessary for maintaining health."
]


# Send claims to RetrievalAgent
results = retrieval_agent.execute(claims)


print("\n=== RETRIEVAL RESULTS ===")

for result in results:

    print("\nClaim:")
    print(result["claim"])

    print("\nLocal Evidence:")

    for i, evidence in enumerate(
        result["local_evidence"],
        start=1
    ):
        print(f"\n--- Evidence {i} ---")
        print("Source:", evidence["source"])
        print("Distance:", evidence["distance"])
        print("Text:")
        print(evidence["text"])

    print("\nWeb Evidence:")
    print(result["web_evidence"])