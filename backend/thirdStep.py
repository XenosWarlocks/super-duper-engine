# project/backend/thirdStep.py
import pandas as pd
import numpy as np

class ThirdStep:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.df = None
        self.debug_mode = False
    
    def enable_debug(self):
        """Enable debug mode to print additional information"""
        self.debug_mode = True
        
    def read_csv(self):
        """Read the CSV file into a pandas DataFrame"""
        try:
            self.df = pd.read_csv(self.csv_file_path)
            print(f"Successfully read CSV file with {len(self.df)} rows")
            if self.debug_mode:
                print("\nSample of posted_time values:")
                print(self.df['posted_time'].value_counts().head())
            return True
        except Exception as e:
            print(f"Error reading CSV file: {str(e)}")
            return False
            
    def remove_old_postings(self):
        """Remove rows where posted_time equals exactly '30+ Days Ago'"""
        if self.df is None:
            return False
            
        try:
            initial_count = len(self.df)
            
            # Find exact matches for '30+ Days Ago'
            mask = self.df['posted_time'] == '30+ Days Ago'
            matching_rows = self.df[mask]
            
            if self.debug_mode and not matching_rows.empty:
                print("\nRows containing exactly '30+ Days Ago':")
                print(matching_rows[['job_title', 'company_name', 'posted_time']])
            
            # Remove the matching rows
            self.df = self.df[~mask]
            
            removed_count = initial_count - len(self.df)
            print(f"Removed {removed_count} rows with '30+ Days Ago' postings")
            
            return True
        except Exception as e:
            print(f"Error removing old postings: {str(e)}")
            return False
            
    def remove_duplicates(self):
        """Remove duplicate entries based on specified columns"""
        if self.df is None:
            return False
            
        try:
            initial_count = len(self.df)
            columns_to_check = ['job_title', 'company_name', 'company_url', 'posted_time']
            
            if self.debug_mode:
                duplicates = self.df[self.df.duplicated(subset=columns_to_check, keep=False)]
                if not duplicates.empty:
                    print("\nExample duplicates before removal:")
                    print(duplicates[columns_to_check].head())
            
            self.df = self.df.drop_duplicates(subset=columns_to_check, keep='first')
            removed_count = initial_count - len(self.df)
            print(f"Removed {removed_count} duplicate entries")
            return True
        except Exception as e:
            print(f"Error removing duplicates: {str(e)}")
            return False
            
    def save_cleaned_data(self, output_file_path=None):
        """Save the cleaned DataFrame to a new CSV file"""
        if self.df is None:
            return False
            
        try:
            if output_file_path is None:
                output_file_path = self.csv_file_path.replace('.csv', '_cleaned.csv')
            
            self.df.to_csv(output_file_path, index=False)
            print(f"Saved cleaned data to {output_file_path}")
            print(f"Final number of rows: {len(self.df)}")
            return True
        except Exception as e:
            print(f"Error saving cleaned data: {str(e)}")
            return False
            
    def process(self):
        """Execute all cleaning steps"""
        print("Starting data cleaning process...")
        if not self.read_csv():
            return False
            
        if not self.remove_old_postings():
            return False
            
        if not self.remove_duplicates():
            return False
            
        if not self.save_cleaned_data():
            return False
        
        print("Data cleaning completed successfully")
        return True