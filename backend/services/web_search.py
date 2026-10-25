from ddgs import DDGS


class WebSearchService:
    """
    Performs web searches for factual claims.
    """

    def __init__(self):
        self.search_engine = DDGS()

    def search(self, query: str, max_results: int = 5):

        results = self.search_engine.text(
            query,
            region="us-en",
            safesearch="moderate",
            max_results=max_results
        )

        web_evidence = []

        for result in results:

            web_evidence.append({
                "title": result.get("title", ""),
                "url": result.get("href", ""),
                "text": result.get("body", ""),
                "source": "web"
            })

        return web_evidence