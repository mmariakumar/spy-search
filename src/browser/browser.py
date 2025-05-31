from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


import time


class Browser:
    GOOGLE_URL = "https://google.com"

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

    def CloseDriver(self):
        self.driver.close()
