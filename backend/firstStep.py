
# project/backend/firstStep.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time

class FirstStep:
    def __init__(self):
        self.driver = None
        
    def setup_driver(self):
        """Setup and return Chrome WebDriver with some basic options"""
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_page_load_timeout(90)
        return self.driver

    def wait_for_page_load(self, initial_wait=60):
        """Wait for the page to be fully loaded with an initial long wait"""
        try:
            print(f"Waiting {initial_wait} seconds for initial page load...")
            time.sleep(initial_wait)
            
            print("Checking if page is fully loaded...")
            WebDriverWait(self.driver, 30).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            print("Page loaded successfully!")
            time.sleep(5)
            return True
        except Exception as e:
            print(f"Error waiting for page load: {str(e)}")
            return False

    def is_element_present(self, css_selector, timeout=20):
        """Check if an element is present and visible on the page"""
        try:
            print(f"Looking for element: {css_selector}")
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))
            )
            print(f"Found element: {css_selector}")
            return element
        except Exception as e:
            print(f"Could not find element {css_selector}: {str(e)}")
            return None

    def execute_search(self, url):
        """Execute the search process"""
        try:
            print(f"Navigating to {url}")
            self.driver.get(url)
            
            if not self.wait_for_page_load():
                print("Page did not load completely after initial wait")
                return False
            
            print("Looking for search input field...")
            search_box = self.is_element_present('div.suggestor-box.flex-row.flex-wrap.bottom input.suggestor-input')
            
            if not search_box:
                print("Trying alternative selectors...")
                selectors = [
                    'input.suggestor-input',
                    '.suggestor-box input',
                    'input[type="text"]'
                ]
                
                for selector in selectors:
                    search_box = self.is_element_present(selector)
                    if search_box:
                        print(f"Found input using selector: {selector}")
                        break
            
            if not search_box:
                print("Could not find search input with any selector")
                return False
            
            print("Inputting search term...")
            search_box.clear()
            time.sleep(2)
            
            search_box.send_keys("Lead Generation")
            time.sleep(2)
            
            print("Pressing Enter key...")
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)
            
            print("Search submitted successfully")
            return True
            
        except Exception as e:
            print(f"Error during search process: {str(e)}")
            return False

    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()

