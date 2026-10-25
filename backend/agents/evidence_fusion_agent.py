from agents.base_agent import BaseAgent


class EvidenceFusionAgent(BaseAgent):
    """
    Combines evidence retrieved from different sources
    into one clean evidence collection.
    """

    def __init__(self):
        super().__init__("Evidence Fusion Agent")

    def execute(self, input_data):
        """
        Expected input:

        {
            "local_evidence": [...],
            "web_evidence": [...]
        }
        """

        local_evidence = input_data.get("local_evidence", [])
        web_evidence = input_data.get("web_evidence", [])

        # Combine both evidence sources
        combined_evidence = local_evidence + web_evidence

        # Remove duplicates
        unique_evidence = []
        seen = set()

        for evidence in combined_evidence:

            text = evidence.get("text", "").strip()

            if not text:
                continue

            # Simple duplicate detection
            key = text.lower()

            if key not in seen:
                seen.add(key)
                unique_evidence.append(evidence)

        return unique_evidence