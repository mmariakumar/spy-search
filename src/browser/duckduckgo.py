import asyncio
import aiohttp
from html import unescape
from langchain_community.tools import DuckDuckGoSearchResults
from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Optional, Set
import time
from functools import lru_cache
import re
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class DuckSearch:
    def __init__(self):
        self.search_engine = DuckDuckGoSearchResults(
            backend="text", output_format="list"
        )
        self.news_engine = DuckDuckGoSearchResults(
            backend="news", output_format="list", num_results=8
        )
        # Global session pool for maximum performance
        self._session_pool: List[aiohttp.ClientSession] = []
        self._session_index = 0
        self._failed_urls: Set[str] = set()
        self._content_cache: Dict[str, str] = {}
        
        # Pre-compile regex patterns for faster text processing
        self._text_cleanup_pattern = re.compile(r'\s+')
        self._html_tag_pattern = re.compile(r'<[^>]+>')

    async def _get_session_pool(self, pool_size: int = 8) -> List[aiohttp.ClientSession]:
        """Create optimized session pool for maximum concurrency"""
        if len(self._session_pool) < pool_size:
            for _ in range(pool_size - len(self._session_pool)):
                # Ultra-aggressive connector settings
                connector = aiohttp.TCPConnector(
                    limit=200,                    # Massive connection pool
                    limit_per_host=50,           # High per-host limit
                    ttl_dns_cache=600,           # Long DNS cache
                    use_dns_cache=True,
                    keepalive_timeout=60,        # Long keepalive
                    enable_cleanup_closed=True,
                    force_close=False,           # Reuse connections
                    ssl=False,                   # Skip SSL verification for speed
                )
                
                # Hyper-aggressive timeouts
                timeout = aiohttp.ClientTimeout(
                    total=1.25,      # Ultra-short total timeout
                    connect=0.5,    # Lightning connect
                    sock_read=0.9   # Fast read
                )
                
                session = aiohttp.ClientSession(
                    connector=connector,
                    timeout=timeout,
                    headers={
                        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
                        "Accept": "text/html,*/*;q=0.9",
                        "Accept-Encoding": "gzip, deflate",
                        "Connection": "keep-alive",
                        "Cache-Control": "no-cache",
                    },
                    read_bufsize=16384,          # Smaller buffer for speed
                    skip_auto_headers={"User-Agent"},
                )
                self._session_pool.append(session)
        
        return self._session_pool

    def _get_next_session(self) -> aiohttp.ClientSession:
        """Round-robin session selection for load balancing"""
        sessions = asyncio.get_event_loop().run_until_complete(self._get_session_pool())
        session = sessions[self._session_index % len(sessions)]
        self._session_index += 1
        return session

    @lru_cache(maxsize=1000)
    def _is_valid_url(self, url: str) -> bool:
        """Fast URL validation with caching"""
        try:
            parsed = urlparse(url)
            return bool(parsed.netloc and parsed.scheme in ('http', 'https'))
        except:
            return False

    async def _extract_full_text_lightning(self, url: str, limit: int = 400) -> str:
        """Lightning-fast text extraction with all optimizations"""
        if not url or url in self._failed_urls:
            return ""
        
        # Check cache first
        if url in self._content_cache:
            return self._content_cache[url]
            
        if not self._is_valid_url(url):
            self._failed_urls.add(url)
            return ""
            
        try:
            session = self._get_next_session()
            
            # Use HEAD request first to check if content is worth fetching
            try:
                async with session.head(url) as head_response:
                    content_type = head_response.headers.get('content-type', '').lower()
                    if not any(ct in content_type for ct in ['html', 'text']):
                        self._failed_urls.add(url)
                        return ""
                    
                    # Skip large files
                    content_length = head_response.headers.get('content-length')
                    if content_length and int(content_length) > 100000:  # Skip files > 100KB
                        self._failed_urls.add(url)
                        return ""
            except:
                pass  # Continue with GET if HEAD fails
            
            # Lightning GET request with streaming
            async with session.get(url) as response:
                if response.status != 200:
                    self._failed_urls.add(url)
                    return ""
                
                # Read only first chunk for speed
                content = b""
                chunk_size = 8192
                async for chunk in response.content.iter_chunked(chunk_size):
                    content += chunk
                    if len(content) > 50000:  # Stop after 50KB
                        break
                
            # Ultra-fast parsing with selectolax (fallback to BeautifulSoup)
            try:
                from selectolax.parser import HTMLParser
                tree = HTMLParser(content)
                paragraphs = tree.css('p')
                texts = [node.text() for node in paragraphs[:30] if node.text()]
            except ImportError:
                # Fallback to BeautifulSoup with fastest parser
                soup = BeautifulSoup(content, "html.parser")  # Fastest built-in parser
                paragraphs = soup.find_all("p", limit=30)
                texts = [p.get_text() for p in paragraphs if p.get_text()]
            
            # Ultra-fast text processing
            if not texts:
                self._failed_urls.add(url)
                return ""
            
            # Join and clean in one pass
            full_text = " ".join(texts)
            # Fast regex cleanup
            full_text = self._html_tag_pattern.sub('', full_text)
            full_text = self._text_cleanup_pattern.sub(' ', full_text)
            full_text = unescape(full_text)[:limit].strip()
            
            # Cache result
            self._content_cache[url] = full_text
            return full_text

        except asyncio.TimeoutError:
            self._failed_urls.add(url)
            return ""
        except Exception:
            self._failed_urls.add(url)
            return ""

    async def _extract_and_update_lightning(self, result: Dict) -> Dict:
        """Lightning-fast result updating"""
        url = result.get("link")
        if not url:
            result["full_content"] = ""
            return result
            
        full_text = await self._extract_full_text_lightning(url)
        result["full_content"] = full_text
        return result

    async def _async_deep_search_lightning(self, results: List[Dict], k: int) -> List[Dict]:
        """State-of-the-art async deep search with maximum concurrency"""
        if not results:
            return []
        
        # Massive concurrency with intelligent batching
        max_concurrent = min(k * 4, 100)  # Scale with request count
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_with_semaphore(result):
            async with semaphore:
                return await self._extract_and_update_lightning(result)
        
        # Pre-filter results to avoid processing bad URLs
        valid_results = []
        for result in results[:k]:
            url = result.get("link", "")
            if url and url not in self._failed_urls and self._is_valid_url(url):
                valid_results.append(result)
            else:
                result["full_content"] = ""
                valid_results.append(result)
        
        if not valid_results:
            return results[:k]
        
        # Create tasks with intelligent batching
        tasks = []
        for result in valid_results:
            if result.get("link") and result.get("link") not in self._failed_urls:
                tasks.append(asyncio.create_task(process_with_semaphore(result)))
            else:
                # Create dummy completed task for results we're skipping
                completed_task = asyncio.create_task(asyncio.sleep(0))
                completed_task.set_result(result)
                tasks.append(completed_task)
        
        try:
            # Ultra-fast processing with short timeout
            start_time = time.time()
            completed_results = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=1.2  # Ultra-aggressive timeout
            )
            
            processing_time = time.time() - start_time
            logger.debug(f"Deep search completed in {processing_time:.2f}s")
            
            # Process results super fast
            final_results = []
            for i, result in enumerate(completed_results):
                if isinstance(result, Exception):
                    # Use original result if processing failed
                    original = valid_results[i] if i < len(valid_results) else results[i]
                    original["full_content"] = ""
                    final_results.append(original)
                else:
                    final_results.append(result)
            
            return final_results[:k]
            
        except asyncio.TimeoutError:
            # Cancel pending tasks immediately
            for task in tasks:
                if not task.done():
                    task.cancel()
            
            logger.debug("Deep search timed out - returning partial results")
            # Return original results with empty content
            for result in valid_results:
                if "full_content" not in result:
                    result["full_content"] = ""
            return valid_results[:k]
            
        except Exception as e:
            logger.debug(f"Deep search error: {e}")
            return results[:k]

    def search_result(
        self, query: str, k: int = 6, backend: str = "text", deep_search: bool = True
    ) -> List[Dict]:
        """State-of-the-art search with maximum performance"""
        start_time = time.time()
        logger.info("Starting lightning search...")
        
        # Get initial results with error handling
        try:
            results = self.search_engine.invoke(query)
        except Exception as e:
            logger.error(f"Search engine error: {e}")
            return []
        
        if not deep_search or not results:
            search_time = time.time() - start_time
            logger.info(f"Basic search completed in {search_time:.2f}s")
            return results[:k]
        
        logger.info("Processing results with lightning speed...")
        
        # Ultra-fast async execution
        try:
            def run_lightning_search():
                # Create isolated event loop for maximum performance
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    return loop.run_until_complete(self._async_deep_search_lightning(results, k))
                finally:
                    loop.close()
            
            # Check if we're in async context
            try:
                asyncio.get_running_loop()
                # In async context - run in thread with minimal overhead
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix="lightning") as executor:
                    future = executor.submit(run_lightning_search)
                    final_results = future.result(timeout=3.0)
            except RuntimeError:
                # No event loop - run directly
                final_results = asyncio.run(self._async_deep_search_lightning(results, k))
            
            search_time = time.time() - start_time
            logger.info(f"Lightning search completed in {search_time:.2f}s")
            return final_results
                
        except Exception as e:
            logger.error(f"Lightning search error: {e}")
            search_time = time.time() - start_time
            logger.info(f"Fallback search completed in {search_time:.2f}s")
            return results[:k]

    def today_new(self, category: str) -> List[Dict]:
        """Lightning-fast news retrieval"""
        category_queries = {
            "technology": "latest technology and science news",
            "finance": "latest finance news", 
            "entertainment": "latest entertainment and culture news",
            "sports": "latest sports news",
            "world": "latest world news",
            "health": "latest health and healthcare news"
        }
        
        query = category_queries.get(category, "latest news")
        return self.news_engine.invoke(query)

    def clear_cache(self):
        """Clear caches for memory management"""
        self._content_cache.clear()
        self._failed_urls.clear()
        self._is_valid_url.cache_clear()

    async def cleanup(self):
        """Lightning cleanup"""
        cleanup_tasks = []
        for session in self._session_pool:
            if not session.closed:
                cleanup_tasks.append(session.close())
        
        if cleanup_tasks:
            await asyncio.gather(*cleanup_tasks, return_exceptions=True)
        
        self._session_pool.clear()
        self.clear_cache()

    def __del__(self):
        """Cleanup on deletion"""
        try:
            if self._session_pool:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    for session in self._session_pool:
                        if not session.closed:
                            loop.create_task(session.close())
        except:
            pass