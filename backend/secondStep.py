# project/backend/secondStep.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import random
import csv
from datetime import datetime

class SecondStep:
    def __init__(self, driver):
        self.driver = driver
        self.companies_data = []
        self.current_page = 1
        self.max_pages = 20  # We'll stop at page 20
        self.jobs_per_page = 20
        self.base_url = "https://www.naukri.com/lead-generation-jobs"
        
    def random_wait(self):
        """Wait for a random time between 10-15 seconds"""
        wait_time = random.uniform(10, 15)
        print(f"Waiting for {wait_time:.2f} seconds...")
        time.sleep(wait_time)

    def get_element_safely(self, parent_element, selector, attribute=None):
        """Safely get element and its attribute/text"""
        try:
            element = parent_element.find_element(By.CSS_SELECTOR, selector)
            if attribute:
                return element.get_attribute(attribute)
            return element.text
        except NoSuchElementException:
            return ""
        except Exception as e:
            print(f"Error getting element {selector}: {str(e)}")
            return ""

    def process_job_card(self, job_id):
        """Process a single job card"""
        try:
            # Find the job card using data-job-id
            job_card = self.driver.find_element(By.CSS_SELECTOR, f'div[data-job-id="{job_id}"]')
            
            # Extract job title
            job_title_elem = job_card.find_element(By.CSS_SELECTOR, "div.row1 a.title")
            job_title = job_title_elem.get_attribute("title")
            
            # Extract company information
            company_elem = job_card.find_element(By.CSS_SELECTOR, "div.row2 span.comp-dtls-wrap a.comp-name")
            company_name = company_elem.get_attribute("title")
            company_url = company_elem.get_attribute("href")
            
            # Get posting time
            posted_time = self.get_element_safely(job_card, "div.row6 span.job-post-day")
            
            # Store the data
            self.companies_data.append({
                'job_id': job_id,
                'job_title': job_title,
                'company_name': company_name,
                'company_url': company_url,
                'posted_time': posted_time,
                'page_number': self.current_page
            })
            
            print(f"Processed job ID: {job_id} - {company_name} - Page {self.current_page}")
            
        except Exception as e:
            print(f"Error processing job ID {job_id}: {str(e)}")

    def get_job_ids_on_page(self):
        """Get all job IDs on current page"""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.srp-jobtuple-wrapper"))
            )
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.srp-jobtuple-wrapper")
            return [card.get_attribute("data-job-id") for card in job_cards if card.get_attribute("data-job-id")]
        except Exception as e:
            print(f"Error getting job IDs: {str(e)}")
            return []

    def navigate_to_page(self, page_number):
        """Navigate to a specific page number"""
        try:
            url = f"{self.base_url}-{page_number}" if page_number > 1 else self.base_url
            url += "?k=lead%20generation"
            print(f"Navigating to page {page_number}: {url}")
            self.driver.get(url)
            return True
        except Exception as e:
            print(f"Error navigating to page {page_number}: {str(e)}")
            return False

    def process_job_listings(self):
        """Process job listings and extract required information"""
        try:
            while self.current_page <= self.max_pages:
                print(f"\nProcessing page {self.current_page}")
                
                # Navigate to the current page
                if not self.navigate_to_page(self.current_page):
                    break
                
                self.random_wait()
                
                # Get all job IDs on current page
                job_ids = self.get_job_ids_on_page()
                
                if not job_ids:
                    print("No job IDs found on page")
                    break
                
                # Ensure we only process exactly 20 jobs per page
                job_ids = job_ids[:self.jobs_per_page]
                
                # Process each job card one by one
                for job_id in job_ids:
                    self.process_job_card(job_id)
                    # Small random wait between jobs to seem more human-like
                    time.sleep(random.uniform(1, 3))
                
                print(f"Completed page {self.current_page}. Jobs processed on this page: {len(job_ids)}")
                
                # Move to next page
                self.current_page += 1
                
        except Exception as e:
            print(f"Error in process_job_listings: {str(e)}")
        
        finally:
            print(f"Total jobs processed: {len(self.companies_data)}")
            print(f"Total pages processed: {self.current_page - 1}")
            
    def save_to_csv(self, filename="companies_data.csv"):
        """Save the collected data to a CSV file"""
        try:
            if not self.companies_data:
                print("No data to save")
                return
                
            fieldnames = ['job_id', 'job_title', 'company_name', 'company_url', 'posted_time', 'page_number']
            
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.companies_data)
                
            print(f"Data saved to {filename}")
            
        except Exception as e:
            print(f"Error saving to CSV: {str(e)}")

# each page has 20 job posts