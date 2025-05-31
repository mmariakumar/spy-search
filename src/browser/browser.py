from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

"""
    Browser class should provide every kinds of interation allow to model to choose which action to perform
"""
class Browser:
    GOOGLE_URL = "https://google.com/"
    ARXIV_URL = "https://arxiv.org/"
    GOOGLE_NEWS_URL = "https://news.google.com/"


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
        links = self.driver.find_elements("tag name", "a")
        for link in links:
            href = link.get_attribute("href")
            title = link.text.strip()  # Text inside the <a> tag
            if href:
                print(f"Title: {title} | Href: {href}")

        # how to get information with browser 
        # do we need vllm here  ? 

    def next_page(self):
        pass 

    def prev_page(self):
        pass 
        
        
    def CloseDriver(self):
        self.driver.close()


if __name__ == "__main__":
    b = Browser()
    b.GoogleSearch("tesla")
    b.CloseDriver()