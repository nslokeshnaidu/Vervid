import ollama

from agents.base_agent import BaseAgent


class VerificationAgent(BaseAgent):
    """
    Verifies factual claims against retrieved local and web evidence.
    """

    def __init__(self):
        super().__init__("Verification Agent")

    def execute(self, claim, evidence):

        # STEP 1: Handle missing evidence
        if not evidence:
            return {
                "verdict": "INSUFFICIENT",
                "reason": "No evidence was retrieved for this claim."
            }

        # STEP 2: Support either a list or a retrieval-result dictionary
        if isinstance(evidence, dict):
            local_evidence = evidence.get("local_evidence", [])
            web_evidence = evidence.get("web_evidence", [])
            evidence = local_evidence + web_evidence

        # STEP 3: Prepare evidence for the LLM
        evidence_text = ""

        for i, item in enumerate(evidence, start=1):

            source_type = item.get(
                "source_type",
                item.get("source", "Unknown")
            )

            title = item.get("title", "")
            url = item.get("url", "")
            text = item.get("text", "")

            evidence_text += (
                f"\n--- Evidence {i} ---\n"
                f"Source type: {source_type}\n"
                f"Title: {title}\n"
                f"URL: {url}\n"
                f"Text: {text}\n"
            )

        # STEP 4: Verification prompt
        prompt = f"""
You are an AI fact-checking verifier.

Evaluate the CLAIM using ONLY the provided EVIDENCE.

CLAIM:
{claim}

EVIDENCE:
{evidence_text}

Choose one verdict:

SUPPORTED:
The evidence directly supports the important parts of the claim.

CONTRADICTED:
The evidence directly conflicts with an important part of the claim.

INSUFFICIENT:
The evidence does not provide enough information to decide.

Important rules:
- Use ONLY the provided evidence.
- Do not use outside knowledge.
- Do not assume missing information.
- Check important qualifiers, conditions, populations,
  numbers, dates, locations, and relationships.
- A claim is NOT supported merely because some words
  or numbers are similar.
- If the evidence refers to a different population,
  condition, or context, do not mark the claim as supported.
- If the evidence is unrelated, use INSUFFICIENT.

Return EXACTLY two lines:

VERDICT: SUPPORTED
REASON: <short explanation>

OR

VERDICT: CONTRADICTED
REASON: <short explanation>

OR

VERDICT: INSUFFICIENT
REASON: <short explanation>
"""

        # STEP 5: Ask Qwen
        response = ollama.chat(
            model="qwen3:1.7b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response["message"]["content"].strip()

        # STEP 6: Parse the response
        verdict = "INSUFFICIENT"
        reason = "The verifier did not return a valid verdict."

        for line in content.splitlines():

            line = line.strip()

            if line.upper().startswith("VERDICT:"):

                extracted_verdict = line.split(
                    ":", 1
                )[1].strip().upper()

                if extracted_verdict in {
                    "SUPPORTED",
                    "CONTRADICTED",
                    "INSUFFICIENT"
                }:
                    verdict = extracted_verdict

            elif line.upper().startswith("REASON:"):

                reason = line.split(
                    ":", 1
                )[1].strip()

        # STEP 7: Return structured result
        return {
            "verdict": verdict,
            "reason": reason
        }