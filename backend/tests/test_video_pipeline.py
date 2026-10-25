from agents.speech_agent import speech_agent
from agents.claim_extraction_agent import ClaimExtractionAgent
from agents.retrieval_agent import RetrievalAgent


# --------------------------------------------------
# Create agents
# --------------------------------------------------

claim_agent = ClaimExtractionAgent()
retrieval_agent = RetrievalAgent()


# --------------------------------------------------
# Video path
# --------------------------------------------------

video_path = "data/videos/test_video.mp4"


# --------------------------------------------------
# STEP 1: Video -> Transcript
# --------------------------------------------------

print("\n==============================")
print("STEP 1: TRANSCRIPTION")
print("==============================")

transcript = speech_agent.execute(video_path)

print("\nTranscript:")
print(transcript)


# --------------------------------------------------
# STEP 2: Transcript -> Claims
# --------------------------------------------------

print("\n==============================")
print("STEP 2: CLAIM EXTRACTION")
print("==============================")

claims = claim_agent.execute(transcript)

print("\nExtracted Claims:")

for i, claim in enumerate(claims, start=1):
    print(f"{i}. {claim}")


# --------------------------------------------------
# STEP 3: Claims -> Local Evidence
# --------------------------------------------------

print("\n==============================")
print("STEP 3: LOCAL RAG RETRIEVAL")
print("==============================")

results = retrieval_agent.execute(claims)


# --------------------------------------------------
# Display results
# --------------------------------------------------

for result in results:

    print("\n========================================")
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