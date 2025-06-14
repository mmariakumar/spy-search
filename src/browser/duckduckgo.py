import asyncio
import aiohttp
from html import unescape
from langchain_community.tools import DuckDuckGoSearchResults
from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Optional, Set, Tuple
import time
from functools import lru_cache
import re
from urllib.parse import urlparse
import threading
import concurrent.futures
from collections import deque
import weakref
import gc
import orjson  # Ultra-fast JSON if available
from selectolax.parser import HTMLParser  # Ultra-fast HTML parser

logger = logging.getLogger(__name__)


class DuckSearch:
    def __init__(self):
        self.search_engine = DuckDuckGoSearchResults(
            backend="text", output_format="list"
        )
        self.news_engine = DuckDuckGoSearchResults(
            backend="news", output_format="list", num_results=8
        )
        
        # Hyper-aggressive session management
        self._session_pool: deque = deque(maxlen=20)
        self._session_lock = threading.Lock()
        self._failed_urls: Set[str] = set()
        self._content_cache: Dict[str, str] = {}
        self._url_cache: Dict[str, bool] = {}
        
        # Pre-compiled regex patterns (compiled once, reused millions of times)
        self._text_cleanup = re.compile(r'\s+')
        self._html_tags = re.compile(r'<[^>]+>')
        self._extract_paragraphs = re.compile(r'<p[^>]*>(.*?)</p>', re.IGNORECASE | re.DOTALL)
        
        # Background session warmup and preloading
        self._warmup_done = False
        self._background_executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=4, thread_name_prefix="bg-duck"
        )
        self._start_background_warmup()
        
        # Ultra-aggressive connection settings
        self._connector_config = {
            'limit': 300,
            'limit_per_host': 100,
            'ttl_dns_cache': 3600,
            'use_dns_cache': True,
            'keepalive_timeout': 120,
            'enable_cleanup_closed': True,
            'force_close': False,
            'ssl': False,
        }
        
        # Lightning timeout settings
        self._timeout_config = aiohttp.ClientTimeout(
            total=0.8,      # Reduced from 1.25
            connect=0.2,    # Reduced from 0.5  
            sock_read=0.6   # Reduced from 0.9
        )

    def _start_background_warmup(self):
        """Pre-warm connections in background"""
        def warmup():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self._warmup_sessions())
                self._warmup_done = True
            except Exception as e:
                logger.debug(f"Warmup error: {e}")
            finally:
                loop.close()
        
        self._background_executor.submit(warmup)

    async def _warmup_sessions(self):
        """Pre-create optimized sessions"""
        tasks = []
        for _ in range(15):  # Pre-create more sessions
            tasks.append(self._create_optimized_session())
        
        sessions = await asyncio.gather(*tasks, return_exceptions=True)
        valid_sessions = [s for s in sessions if isinstance(s, aiohttp.ClientSession)]
        
        with self._session_lock:
            self._session_pool.extend(valid_sessions)

    async def _create_optimized_session(self) -> aiohttp.ClientSession:
        """Create ultra-optimized session"""
        connector = aiohttp.TCPConnector(**self._connector_config)
        
        session = aiohttp.ClientSession(
            connector=connector,
            timeout=self._timeout_config,
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
                "Accept": "text/html,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "DNT": "1",
            },
            read_bufsize=32768,  # Larger buffer for better throughput
            skip_auto_headers={"User-Agent"},
            connector_owner=False,  # Don't auto-close connector
        )
        return session

    def _get_session_fast(self) -> aiohttp.ClientSession:
        """Ultra-fast session retrieval with fallback"""
        with self._session_lock:
            if self._session_pool:
                session = self._session_pool.popleft()
                # Immediately put it back for reuse
                self._session_pool.append(session)
                return session
        
        # Emergency fallback - create session synchronously
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self._create_optimized_session())

    @lru_cache(maxsize=2000)
    def _is_valid_url_cached(self, url: str) -> bool:
        """Cached URL validation"""
        if url in self._url_cache:
            return self._url_cache[url]
        
        try:
            parsed = urlparse(url)
            is_valid = bool(parsed.netloc and parsed.scheme in ('http', 'https'))
            self._url_cache[url] = is_valid
            return is_valid
        except:
            self._url_cache[url] = False
            return False

    async def _extract_content_blazing(self, url: str, limit: int = 350) -> str:
        """Blazing fast content extraction with all optimizations"""
        if not url or url in self._failed_urls:
            return ""
        
        # Memory cache check
        if url in self._content_cache:
            return self._content_cache[url]
            
        if not self._is_valid_url_cached(url):
            self._failed_urls.add(url)
            return ""
        
        session = self._get_session_fast()
        
        try:
            # Skip HEAD request - go straight to GET for speed
            async with session.get(url, allow_redirects=False) as response:
                if response.status not in (200, 301, 302):
                    self._failed_urls.add(url)
                    return ""
                
                # Handle redirects manually for speed
                if response.status in (301, 302):
                    redirect_url = response.headers.get('Location')
                    if redirect_url and len(redirect_url) < 200:  # Avoid redirect loops
                        return await self._extract_content_blazing(redirect_url, limit)
                
                # Lightning-fast chunked reading
                content = b""
                async for chunk in response.content.iter_chunked(16384):
                    content += chunk
                    if len(content) > 40000:  # Stop early
                        break
            
            # Ultra-fast parsing with selectolax (much faster than BeautifulSoup)
            try:
                tree = HTMLParser(content)
                # Get paragraphs using CSS selector (fastest method)
                paragraphs = tree.css('p')
                texts = []
                for i, node in enumerate(paragraphs):
                    if i >= 25:  # Limit iterations
                        break
                    text = node.text()
                    if text and len(text) > 20:  # Only meaningful text
                        texts.append(text)
                        if len(' '.join(texts)) > limit:  # Early exit
                            break
                            
            except Exception:
                # Ultra-fast regex fallback (faster than BeautifulSoup)
                content_str = content.decode('utf-8', errors='ignore')
                matches = self._extract_paragraphs.findall(content_str)
                texts = [self._html_tags.sub('', match).strip() for match in matches[:25]]
                texts = [t for t in texts if len(t) > 20]
            
            if not texts:
                self._failed_urls.add(url)
                return ""
            
            # Lightning text processing
            full_text = " ".join(texts)
            full_text = self._text_cleanup.sub(' ', unescape(full_text))
            full_text = full_text[:limit].strip()
            
            # Cache with memory management
            if len(self._content_cache) > 500:
                # Remove oldest 100 entries
                old_keys = list(self._content_cache.keys())[:100]
                for key in old_keys:
                    del self._content_cache[key]
            
            self._content_cache[url] = full_text
            return full_text

        except (asyncio.TimeoutError, aiohttp.ClientError):
            self._failed_urls.add(url)
            return ""
        except Exception:
            self._failed_urls.add(url)
            return ""

    async def _process_result_blazing(self, result: Dict) -> Dict:
        """Lightning result processing"""
        url = result.get("link")
        if not url or url in self._failed_urls:
            result["full_content"] = ""
            return result
            
        content = await self._extract_content_blazing(url)
        result["full_content"] = content
        return result

    async def _deep_search_blazing(self, results: List[Dict], k: int) -> List[Dict]:
        """Blazing fast deep search with maximum concurrency"""
        if not results:
            return []
        
        # Extreme concurrency with intelligent resource management
        max_concurrent = min(k * 6, 150)  # Even more aggressive
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_with_semaphore(result):
            async with semaphore:
                return await self._process_result_blazing(result)
        
        # Pre-filter and prepare results
        valid_results = []
        tasks = []
        
        for result in results[:k]:
            url = result.get("link", "")
            if url and url not in self._failed_urls and self._is_valid_url_cached(url):
                task = asyncio.create_task(process_with_semaphore(result))
                tasks.append(task)
                valid_results.append(result)
            else:
                result["full_content"] = ""
                valid_results.append(result)
                # Create dummy completed task
                dummy_task = asyncio.create_task(asyncio.sleep(0))
                dummy_task.set_result(result)
                tasks.append(dummy_task)
        
        if not tasks:
            return results[:k]
        
        try:
            # Ultra-aggressive timeout
            start_time = time.time()
            completed = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=0.9  # Reduced from 1.2
            )
            
            processing_time = time.time() - start_time
            logger.debug(f"Blazing search: {processing_time:.3f}s")
            
            # Fast result processing
            final_results = []
            for i, result in enumerate(completed):
                if isinstance(result, Exception):
                    original = valid_results[i] if i < len(valid_results) else results[i]
                    original["full_content"] = ""
                    final_results.append(original)
                else:
                    final_results.append(result)
            
            return final_results[:k]
            
        except asyncio.TimeoutError:
            # Instant task cancellation
            cancelled = 0
            for task in tasks:
                if not task.done():
                    task.cancel()
                    cancelled += 1
            
            logger.debug(f"Timeout - cancelled {cancelled} tasks")
            
            # Return partial results immediately
            for result in valid_results:
                if "full_content" not in result:
                    result["full_content"] = ""
            return valid_results[:k]

    def search_result(
        self, query: str, k: int = 6, backend: str = "text", deep_search: bool = True
    ) -> List[Dict]:
        """Blazing fast search with maximum performance"""
        start_time = time.time()
        logger.info("Starting blazing search...")
        
        # Get initial results
        try:
            results = self.search_engine.invoke(query)
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
        
        if not deep_search or not results:
            search_time = time.time() - start_time
            logger.info(f"⚡ Basic search: {search_time:.3f}s")
            return results[:k]
        
        logger.info("Deep processing...")
        
        # Ultra-fast async execution with optimized event loop handling
        try:
            # Check if we're already in an async context
            try:
                current_loop = asyncio.get_running_loop()
                # Use thread pool for isolation and maximum speed
                with concurrent.futures.ThreadPoolExecutor(
                    max_workers=1, 
                    thread_name_prefix="blazing"
                ) as executor:
                    def run_isolated():
                        # Create dedicated event loop for maximum performance
                        isolated_loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(isolated_loop)
                        try:
                            return isolated_loop.run_until_complete(
                                self._deep_search_blazing(results, k)
                            )
                        finally:
                            isolated_loop.close()
                    
                    future = executor.submit(run_isolated)
                    final_results = future.result(timeout=2.0)  # Reduced timeout
                    
            except RuntimeError:
                # No event loop - run directly with optimizations
                final_results = asyncio.run(
                    self._deep_search_blazing(results, k),
                    debug=False  # Disable debug for speed
                )
            
            search_time = time.time() - start_time
            logger.info(f"🚀 Blazing search complete: {search_time:.3f}s")
            return final_results
                
        except Exception as e:
            logger.error(f"Blazing search error: {e}")
            search_time = time.time() - start_time
            logger.info(f"⚡ Fallback complete: {search_time:.3f}s")
            return results[:k]


    def today_new(self, category: str) -> List[Dict]:
        """Lightning news retrieval"""
        category_queries = {
            "technology": "latest tech science AI news",
            "finance": "latest finance market news", 
            "entertainment": "latest entertainment culture news",
            "sports": "latest sports news",
            "world": "latest world breaking news",
            "health": "latest health medical news"
        }
        
        query = category_queries.get(category, "latest breaking news")
        return self.news_engine.invoke(query)

    def clear_cache(self):
        """Aggressive cache clearing"""
        self._content_cache.clear()
        self._failed_urls.clear()
        self._url_cache.clear()
        self._is_valid_url_cached.cache_clear()
        gc.collect()  # Force garbage collection

    async def cleanup(self):
        """Ultra-fast cleanup"""
        cleanup_tasks = []
        
        with self._session_lock:
            sessions_to_close = list(self._session_pool)
            self._session_pool.clear()
        
        for session in sessions_to_close:
            if not session.closed:
                cleanup_tasks.append(session.close())
        
        if cleanup_tasks:
            await asyncio.gather(*cleanup_tasks, return_exceptions=True)
        
        self.clear_cache()
        
        # Shutdown background executor
        self._background_executor.shutdown(wait=False)

    def __del__(self):
        """Fast cleanup on deletion"""
        try:
            if hasattr(self, '_session_pool') and self._session_pool:
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        # Schedule cleanup without waiting
                        for session in self._session_pool:
                            if not session.closed:
                                loop.create_task(session.close())
                except:
                    pass
            
            if hasattr(self, '_background_executor'):
                self._background_executor.shutdown(wait=False)
        except:
            pass