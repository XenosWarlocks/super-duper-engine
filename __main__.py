
import os
import sys

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_dir not in sys.path:
    sys.path.append(project_dir)

from naukri.backend.firstStep import FirstStep
from naukri.backend.secondStep import SecondStep
from naukri.backend.thirdStep import ThirdStep
import time

def check_existing_csv(file_path):
    """
    Check if CSV file already exists and is not empty
    Returns:
        - True if file exists and is not empty
        - False if file doesn't exist or is empty
    """
    try:
        if os.path.exists(file_path):
            # Check if file is not empty (size > 0 bytes)
            if os.path.getsize(file_path) > 0:
                print(f"Found existing CSV file at {file_path}")
                return True
            else:
                print(f"CSV file exists but is empty at {file_path}")
                return False
        else:
            print(f"No existing CSV file found at {file_path}")
            return False
    except Exception as e:
        print(f"Error checking CSV file: {str(e)}")
        return False

def run_data_collection(csv_file_path):
    """Run the first and second steps to collect data"""
    first_step = FirstStep()
    
    try:
        # Setup driver
        driver = first_step.setup_driver()
        
        # Execute first step
        url = "https://www.naukri.com/"
        if not first_step.execute_search(url):
            print("First step failed")
            return False
            
        print("First step completed successfully")
        
        # Initialize and execute second step
        second_step = SecondStep(driver)
        second_step.process_job_listings()
        second_step.save_to_csv(csv_file_path)
        
        print("Second step completed successfully")
        return True
        
    except Exception as e:
        print(f"Error in data collection: {str(e)}")
        return False
        
    finally:
        # Clean up
        first_step.cleanup()

def run_data_cleaning(csv_file_path):
    """Run the third step to clean the data"""
    try:
        print("\nStarting data cleaning process...")
        third_step = ThirdStep(csv_file_path)
        if third_step.process():
            print("Data cleaning completed successfully")
            return True
        else:
            print("Data cleaning failed")
            return False
    except Exception as e:
        print(f"Error in data cleaning: {str(e)}")
        return False

def main():
    csv_file_path = "companies_data.csv"
    
    try:
        # Check if we already have the CSV file
        if check_existing_csv(csv_file_path):
            print("Existing CSV file found. Skipping data collection steps...")
            # Skip to data cleaning
            if not run_data_cleaning(csv_file_path):
                print("Failed to clean existing data")
                return
        else:
            print("No existing CSV file found. Starting data collection...")
            # Run data collection
            if not run_data_collection(csv_file_path):
                print("Failed to collect data")
                return
            
            # Run data cleaning on newly collected data
            if not run_data_cleaning(csv_file_path):
                print("Failed to clean collected data")
                return
        
        print("\nAll steps completed successfully!")
        
    except Exception as e:
        print(f"An error occurred in main process: {str(e)}")

if __name__ == "__main__":
    main()

# python __main__.py 
