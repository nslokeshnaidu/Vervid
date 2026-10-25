from services.claim_extractor import extract_claims

transcript = """
Hello everyone.

India has 28 states.

I love Bangalore.

The Earth revolves around the Sun.

Subscribe to my channel.
"""

claims = extract_claims(transcript)

print(claims)
