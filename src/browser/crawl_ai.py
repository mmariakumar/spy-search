# we may use crew_ai write some api for it

class Crawl:
    """
    Crawl4ai should be used to support browser.py
    with browser.py search some well known website for example google arxiv google scholar
    or some user self defined website --> seach all link

    --> then use crawl4ai to help for search

    Expected API list
        get_links: given a url which is the result from a search website like google return the result list of that page
        get_images: get all images from the webpage
        get_content: get relevant content to a markdown

        
    """

    def __init__(self, model):
        pass

if __name__ == "__main__":
    import asyncio
    from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

    async def main():
        browser_conf = BrowserConfig(headless=True)  # or False to see the browser
        run_conf = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
        )

        async with AsyncWebCrawler(config=browser_conf) as crawler:
            result = await crawler.arun(url="https://google.com", config=run_conf)
            print(result.markdown)

    asyncio.run(main())
