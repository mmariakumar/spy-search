import re
import requests
from html import unescape
from langchain_community.tools import DuckDuckGoSearchResults


class DuckSearch:
    def __init__(self):
        self.search_engine = DuckDuckGoSearchResults(backend="text", output_format="list")
        self.news_engine = DuckDuckGoSearchResults(backend="news", output_format="list", num_results=9)

    def _extract_full_text(self, url: str, limit: int = 3000) -> str:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=5)
            html = response.text

            # Extract content inside <p> tags using regex
            paragraphs = re.findall(r"<p.*?>(.*?)</p>", html, re.DOTALL | re.IGNORECASE)

            # Clean and join paragraphs
            text = " ".join(unescape(re.sub(r"<.*?>", "", p)).strip() for p in paragraphs)
            return text.strip()[:limit]
        except Exception as e:
            print(f"[ERROR] Failed to fetch {url} -> {e}")
            return ""

    def search_result(self, query: str, k: int = 5, backend: str = "text") -> list:
        results = self.search_engine.invoke(query)
        for result in results[:k]:
            url = result.get("link")
            full_text = self._extract_full_text(url)
            result["full_content"] = full_text
        return results[:k]

    def today_new(self, category: str) -> list:
        if category == "technology":
            category_query = "latest technology and science news"
        elif category == "finance":
            category_query = "latest finance news"
        elif category == "entertainment":
            category_query = "latest entertainment and culture news"
        elif category == "sports":
            category_query = "latest sports news"
        elif category == "world":
            category_query = "latest world news"
        elif category == "health":
            category_query = "latest health and healthcare news"
        else:
            category_query = "latest news"
        return self.news_engine.invoke(category_query)
