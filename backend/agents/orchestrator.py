from agents.speech_agent import speech_agent
from agents.claim_extraction_agent import ClaimExtractionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.verification_agent import VerificationAgent

from models.analysis_result import AnalysisResult


class Orchestrator:
    """
    Coordinates the VeriVid fact-checking pipeline.
    """

    def __init__(self):

        self.speech_agent = speech_agent
        self.claim_agent = ClaimExtractionAgent()
        self.retrieval_agent = RetrievalAgent()
        self.verification_agent = VerificationAgent()

    def analyze_video(self, video_path):

        # ------------------------------------------
        # STEP 1: Video -> Transcript
        # ------------------------------------------

        transcript = self.speech_agent.execute(video_path)

        # ------------------------------------------
        # STEP 2: Transcript -> Claims
        # ------------------------------------------

        claims = self.claim_agent.execute(transcript)

        # Make sure claims is a list
        if isinstance(claims, str):
            claims = [
                claim.strip("-• ").strip()
                for claim in claims.splitlines()
                if claim.strip()
            ]

        # ------------------------------------------
        # STEP 3: Claims -> Retrieved Evidence
        # ------------------------------------------

        retrieval_results = self.retrieval_agent.execute(claims)

        # ------------------------------------------
        # STEP 4: Evidence -> Verification
        # ------------------------------------------

        verification_results = []

        for result in retrieval_results:

            claim = result["claim"]

            # Add source labels to local evidence
            local_evidence = [
                {**item, "source_type": "LOCAL RAG"}
                for item in result.get("local_evidence", [])
            ]

            # Add source labels to web evidence
            web_evidence = [
                {**item, "source_type": "WEB"}
                for item in result.get("web_evidence", [])
            ]

            evidence = local_evidence + web_evidence

            verification = self.verification_agent.execute(
                claim=claim,
                evidence=evidence
            )

            verification_results.append({
                "claim": claim,
                "verification": verification
            })

        # ------------------------------------------
        # STEP 5: Calculate Trust Score
        # ------------------------------------------

        supported = 0
        contradicted = 0
        insufficient = 0

        for item in verification_results:

            verdict = item["verification"]["verdict"]

            if verdict == "SUPPORTED":
                supported += 1

            elif verdict == "CONTRADICTED":
                contradicted += 1

            else:
                insufficient += 1

        total_claims = len(verification_results)
        decisive_claims = supported + contradicted

        trust_score = (
            round((supported / decisive_claims) * 100, 2)
            if decisive_claims > 0
            else None
        )

        coverage = (
            round((decisive_claims / total_claims) * 100, 2)
            if total_claims > 0
            else 0
        )

        # ------------------------------------------
        # STEP 6: Create Final Analysis Result
        # ------------------------------------------

        result = AnalysisResult(
            transcript=transcript,
            claims=claims,
            evidence=retrieval_results,
            verification=verification_results,
            report={
                "trust_score": trust_score,
                "coverage": coverage,
                "total_claims": total_claims,
                "supported": supported,
                "contradicted": contradicted,
                "insufficient": insufficient
            }
        )

        return result