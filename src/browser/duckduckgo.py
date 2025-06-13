import re
import requests
from html import unescape
from langchain_community.tools import DuckDuckGoSearchResults
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed , wait
import aiohttp
import asyncio

from functools import lru_cache

import time 

import logging 
logger = logging.getLogger(__name__)

class DuckSearch:
    def __init__(self):
        self.search_engine = DuckDuckGoSearchResults(backend="text", output_format="list")
        self.news_engine = DuckDuckGoSearchResults(backend="news", output_format="list", num_results=9)
        
    @lru_cache(maxsize=1000)
    def _extract_full_text(self, url: str, limit: int = 200) -> str:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            # Use session for connection reuse
            with requests.Session() as session:
                response = session.get(url, headers=headers, timeout=0.55, stream=True)
                response.raise_for_status()

                # Read only first 100KB to avoid huge downloads (adjust size as needed)
                content = b""
                max_bytes = 40 * 1024  # 100 KB
                for chunk in response.iter_content(chunk_size=1024):
                    content += chunk
                    if len(content) >= max_bytes:
                        break
                # Use lxml parser for speed (fall back to html.parser if lxml not installed)
                try:
                    soup = BeautifulSoup(content, "lxml")
                except Exception:
                    soup = BeautifulSoup(content, "html.parser")

                paragraphs = soup.find_all("p")
                texts = []
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if text:
                        texts.append(unescape(text))
                        # Early stop if we exceed limit to avoid unnecessary processing
                        if sum(len(t) for t in texts) > limit:
                            break
                combined_text = " ".join(texts)
                logger.info(combined_text)
                return combined_text[:limit].strip()

        except Exception as e:
            logger.error(f"[ERROR] Failed to fetch {url} -> {e}")
            return ""

    async def search_result(self, query: str, k: int = 5, backend: str = "text", deep_search: bool = True) -> list:
        logger.info("start searching... ")
        results = self.search_engine.invoke(query)

        if deep_search:
            updated_results = await deep_search_async(results, k)
            results[:k] = updated_results

        logger.info("end searching ...")
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
    

async def _extract_full_text_async(session, url):
    async with session.get(url, timeout=2) as response:
        return await response.text()

async def _extract_and_update_async(session, result):
    url = result.get("link")
    if not url:
        return result
    full_text = await _extract_full_text_async(session, url)
    result["full_content"] = full_text
    return result

async def deep_search_async(results, k):
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(_extract_and_update_async(session, res)) for res in results[:k]]
        updated_results = []
        for task in asyncio.as_completed(tasks):
            try:
                updated_results.append(await asyncio.wait_for(task, timeout=0.5))
            except asyncio.TimeoutError:
                logger.warning("[WARN] Extraction timed out for one of the results.")
            except Exception as e:
                logger.error(f"[ERROR] Exception during deep search extraction: {e}")
        return updated_results