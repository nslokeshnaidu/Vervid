from agents.orchestrator import Orchestrator


orchestrator = Orchestrator()


video_path = "data/videos/test_video.mp4"


print("\n==============================")
print("STARTING VERIVID PIPELINE")
print("==============================")


result = orchestrator.analyze_video(video_path)


print("\n==============================")
print("TRANSCRIPT")
print("==============================")

print(result.transcript)


print("\n==============================")
print("CLAIMS")
print("==============================")

for i, claim in enumerate(result.claims, start=1):

    print(f"{i}. {claim}")


print("\n==============================")
print("VERIFICATION")
print("==============================")

for item in result.verification:

    print("\nCLAIM:")
    print(item["claim"])

    print("\nRESULT:")
    print(item["verification"])