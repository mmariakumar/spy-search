from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

import time
import random

"""
    Browser class should provide every kinds of interation allow to model to choose which action to perform

    Brower should have the follwoing methods 
    - Scroll Up 
    - Scrool Down 
    - Access specific link
    - Print Screen
    - Access to next page
    - print screen
    - get text from the current web page []
    - switch tab [done , refactor need]
    - open multiple tab [done] 
    - next page [done] 
    - previous page [done]

"""
class Browser:
    GOOGLE_URL = "https://google.com/"
    ARXIV_URL = "https://arxiv.org/"
    GOOGLE_NEWS_URL = "https://news.google.com/"
    GOOGLE_SCHOLAR = "https://scholar.google.com"

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

    def GoogleSearch(self, query: str):
        self.driver.get(Browser.GOOGLE_URL)
        search_bar = self.driver.find_element(By.ID, "APjFqb")
        search_bar.send_keys(query)
        time.sleep(1.5)  # avoid bot detection
        search_bar.send_keys(Keys.RETURN)
        time.sleep(3)

        element = self.driver.find_element(By.TAG_NAME , "body")
        # we have to use beautiful soup here

    def get_search_content(self):
        """
        Parses the HTML source of a Google search results page to extract
        the title, link, and description of each search result.

        Returns:
            list: A list of dictionaries, where each dictionary contains:
                  'title' (str): The title of the search result.
                  'link' (str): The URL of the search result.
                  'description' (str): The description snippet of the search result.
        """
        src = self.driver.page_source
        soup = BeautifulSoup(src, "html.parser")

        results = []

        # Google's HTML structure for search results can change.
        # These selectors are based on common patterns observed.
        # 'div.MjjYud' is a common container for individual search results.
        # 'div.g' is an older but sometimes still relevant container.
        # 'div.hlcw0c' is another observed container.
        # We select them together; you might need to adjust or prioritize if nesting causes issues.
        search_result_blocks = soup.select('div.MjjYud, div.g, div.hlcw0c')
        
        if not search_result_blocks:
            # Fallback for a different structure, e.g. some pages use 'div.srg div.g'
            # or if the main selectors fail, try a more general approach (less reliable)
            # search_result_blocks = soup.select('div.srg div.g') # Example fallback
            pass # Keep it simple for now, rely on the primary selectors

        for block in search_result_blocks:
            link_url = None
            description_text = None
            title_text = None

            # --- Extract Link and Title ---
            # Common pattern: Link and title are in an <a> tag, often within a <div> with class 'yuRUbf'
            # The <a> tag itself often contains an <h3> tag for the title.
            link_tag_candidate = block.select_one('div.yuRUbf a[href]')

            if not link_tag_candidate:
                # Fallback: Look for an <a> tag that has an <h3> child directly within the block
                link_tag_candidate = block.select_one('a[href]:has(h3)')
            
            if not link_tag_candidate:
                # Fallback: Look for an <a> tag with a 'data-ved' attribute, which are common on result links
                link_tag_candidate = block.select_one('a[href][data-ved]')
            if link_tag_candidate:
                link_url = link_tag_candidate.get('href')
                # Clean Google's redirect URLs (e.g., /url?q=REAL_URL&sa=...)
                if link_url and link_url.startswith('/url?q='):
                    try:
                        parsed_url = urlparse(link_url)
                        actual_url = parse_qs(parsed_url.query).get('q')
                        if actual_url:
                            link_url = actual_url[0]
                    except Exception as e:
                        # If parsing fails, keep the original link_url
                        # print(f"Could not parse redirect URL: {link_url} - {e}")
                        pass
                # Extract title
                title_tag = link_tag_candidate.find('h3')
                if title_tag:
                    title_text = title_tag.get_text(strip=True)
                else:
                    # If no <h3> inside <a>, try to get text from <a> directly,
                    # or from a specific child span if that's the structure.
                    # Example: Google sometimes puts title in <a ...><div ...><span...>TITLE</span></div></a>
                    title_span_candidate = link_tag_candidate.select_one('div > span') # Adjust if needed
                    if title_span_candidate:
                         title_text = title_span_candidate.get_text(strip=True)
                    if not title_text: # Fallback to the whole link text if specific title parts not found
                         title_text = link_tag_candidate.get_text(strip=True).splitlines()[0] # Get first line
            description_selectors = [
                "div.VwiC3b span",    # Text often directly in a span child of VwiC3b
                "div.VwiC3b",         # Or directly in VwiC3b if no specific span
                "div.IsZvec",
                "div.MUxGbd",
                "div.s3v9rd",         # Another observed class for snippets
                "div[role='text']"    # Some snippets might use ARIA roles
            ]
            description_tag = None
            for selector in description_selectors:
                candidate = block.select_one(selector)
                if candidate and candidate.get_text(strip=True): # Ensure it has some text
                    description_tag = candidate
                    break
            if description_tag:
                description_text = description_tag.get_text(separator=' ', strip=True)
            # --- Add to results if essential parts are found ---
            if link_url and description_text:
                # Basic sanity checks to filter out irrelevant links or very short/empty content
                if link_url.startswith('http') and \
                   not any(domain in link_url for domain in [
                       "google.com/search?q=", 
                       "google.com/webhp",
                       "google.com/imgres",
                       "accounts.google.com",
                       "support.google.com", # Often not a primary search result
                       "maps.google.com" # Usually has its own block type
                   ]) and \
                   not link_url.startswith("/search?q=") and \
                   len(description_text) > 20: # Ensure description is somewhat substantial
                    
                    results.append({
                        'title': title_text if title_text else "N/A",
                        'link': link_url,
                        'description': description_text
                    })
        return results


    def switch_tab(self , n:int):
        all_tabls = self._get_all_handler()
        self.driver.switch_to.window(all_tabls[n])
    
    def new_tab(self):
        self.driver.switch_to.new_window('tab')
        self.driver.get("https://google.com") #default set to be google 

    def next_page(self):
        time.sleep(random.random()*3)
        self.driver.forward()

    def prev_page(self):
        time.sleep(random.random()*3) # one to three seconds random
        self.driver.back()

    def access_url(self , url):
        self.driver.get(url)

    def CloseDriver(self):
        self.driver.close()

    def _get_all_handler(self):
        # maybe we have to refactor here such that a map {description : tab name}
        all_handler = self.driver.window_handles
        return all_handler


if __name__ == "__main__":
    b = Browser()
    b.GoogleSearch("tesla")
    b.get_content()
    time.sleep(1)
    b.CloseDriver()
