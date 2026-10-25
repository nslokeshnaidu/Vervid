import re

from agents.base_agent import BaseAgent
from services.vector_db import VectorDBService
from services.web_search import WebSearchService


class RetrievalAgent(BaseAgent):
    """
    Retrieves evidence from local RAG and the web,
    then ranks it using simple keyword overlap.
    """

    def __init__(self):
        super().__init__("Retrieval Agent")

        self.vector_db = VectorDBService()
        self.web_search = WebSearchService()

    def _get_keywords(self, text):
        """Extract meaningful words for basic relevance matching."""

        stopwords = {
            "the", "is", "are", "was", "were", "a", "an", "and",
            "or", "of", "to", "in", "on", "for", "with", "by",
            "from", "that", "this", "it", "as", "at", "be",
            "has", "have", "had", "do", "does", "did"
        }

        words = re.findall(r"\b[a-zA-Z0-9.]+\b", text.lower())

        return {
            word for word in words
            if word not in stopwords and len(word) > 1
        }

    def _rank_evidence(self, claim, evidence):
        """
        Rank evidence by the proportion of claim keywords
        that also appear in the evidence.
        """

        claim_keywords = self._get_keywords(claim)

        if not claim_keywords:
            return evidence

        ranked = []

        for index, item in enumerate(evidence):

            evidence_text = " ".join([
                str(item.get("title", "")),
                str(item.get("text", "")),
            ])

            evidence_keywords = self._get_keywords(evidence_text)

            overlap = claim_keywords.intersection(evidence_keywords)
            score = len(overlap) / len(claim_keywords)

            ranked.append((score, index, item))

        # Higher keyword overlap first.
        # Original order is preserved when scores are equal.
        ranked.sort(key=lambda x: (-x[0], x[1]))

        return [item for score, index, item in ranked]

    def execute(self, claims):

        results = []

        for claim in claims:

            # --------------------------------------
            # STEP 1: Retrieve local evidence
            # --------------------------------------

            local_evidence = self.vector_db.search(
                query=claim,
                top_k=5
            )

            # --------------------------------------
            # STEP 2: Retrieve web evidence
            # --------------------------------------

            web_evidence = self.web_search.search(
                query=claim,
                max_results=5
            )

            # --------------------------------------
            # STEP 3: Rank each source separately
            # --------------------------------------

            local_evidence = self._rank_evidence(
                claim,
                local_evidence
            )

            web_evidence = self._rank_evidence(
                claim,
                web_evidence
            )

            # --------------------------------------
            # STEP 4: Store results
            # --------------------------------------

            results.append({
                "claim": claim,
                "local_evidence": local_evidence,
                "web_evidence": web_evidence
            })

        return results