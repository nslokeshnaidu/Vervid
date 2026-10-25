import json
import ollama

from agents.base_agent import BaseAgent


class ClaimExtractionAgent(BaseAgent):
    """
    Extracts every individual factual claim from a transcript.
    """

    def __init__(self):
        super().__init__("Claim Extraction Agent")

    def execute(self, transcript: str):

        prompt = f"""
You are the claim extraction component of an AI fact-checking system.

Your job is to extract EVERY factual claim from the transcript.

IMPORTANT RULES:

1. Extract EVERY factual assertion.
2. Do NOT skip a claim because it sounds false.
3. Do NOT correct or fact-check anything.
4. If one sentence contains multiple factual assertions,
   split them into separate claims.
5. Each claim must contain ONE factual assertion.
6. Preserve names, places, numbers, dates, and relationships.
7. Do not combine unrelated claims.
8. Ignore greetings, opinions, questions, jokes,
   advertisements, and calls to action.
9. Do not invent information that is not present
   in the transcript.

Example:

Transcript:
"Delhi is the capital of India and Mumbai is the
capital of Maharashtra."

Correct output:
[
    "Delhi is the capital of India.",
    "Mumbai is the capital of Maharashtra."
]

Return ONLY valid JSON in exactly this format:

{{
    "claims": [
        "claim 1",
        "claim 2",
        "claim 3"
    ]
}}

Transcript:
{transcript}
"""

        response = ollama.chat(
            model="qwen3:1.7b",
            format="json",
            options={
                "temperature": 0
            },
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response["message"]["content"].strip()

        try:

            data = json.loads(content)

            claims = data.get("claims", [])

            if not isinstance(claims, list):
                return []

            cleaned_claims = []

            for claim in claims:

                if isinstance(claim, str):

                    claim = claim.strip()

                    if claim:
                        cleaned_claims.append(claim)

            return cleaned_claims

        except (json.JSONDecodeError, AttributeError, TypeError):

            print("Claim extraction returned invalid JSON:")
            print(content)

            return []