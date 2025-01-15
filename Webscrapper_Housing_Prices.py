# Report: Housing Price Trends in Cape Town

# Summary and Objectives
# This script extracts tabular data from the Property24 website for Cape Town City Centre using Selenium and writes it into an Excel report. 
# The primary objectives of this project are to:
# 1. Automate the extraction of property trends data for analysis.
# 2. Create a structured Excel report containing tables with insights on property prices, trends, and other relevant metrics.
# 3. Enable further data analysis on housing trends in Cape Town.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Define URL and Table IDs
p24_url = 'https://www.property24.com/cape-town/cape-town-city-centre/property-trends/9138'

ids = [
    'annualSaleAndListingTrendsGraph',
    'totalNumberOfPropertiesTable',
    'averageListPriceVsBedroomsGraph',
    'soldPropertiesGraph_Popular1',
    'soldPropertiesGraph_Popular2',
    'ageProfileGraph'
]

# Function to divide rows into chunks based on column size
def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

# Configure WebDriver (Headless Chrome)
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
browser = webdriver.Chrome(options=options)

try:
    # Open the webpage
    browser.get(p24_url)
    wait = WebDriverWait(browser, 10)

    # Open Excel writer
    with pd.ExcelWriter('Housing_Prices_Cape_Town_Output.xlsx', engine='xlsxwriter') as writer:
        for id in ids:
            try:
                # Wait for the table to load
                wait.until(EC.presence_of_element_located((By.ID, id)))
                
                # Get headers and rows
                columns = list(map(lambda el: el.get_attribute("textContent"), 
                                   browser.find_elements(By.XPATH, f'//*[@id="{id}"]//table//thead//tr//th')))
                rows = list(map(lambda el: el.get_attribute("textContent"), 
                                browser.find_elements(By.XPATH, f'//*[@id="{id}"]//table//tbody//tr//td')))

                # Validate and process table data
                if len(columns) == 0 or len(rows) == 0:
                    print(f"Table with ID '{id}' is empty or invalid.")
                    continue

                if len(rows) % len(columns) != 0:
                    print(f"Mismatch in table structure for ID '{id}'")
                    continue

                # Write to Excel
                df = pd.DataFrame(divide_chunks(rows, len(columns)), columns=columns)
                df.to_excel(writer, sheet_name=id, index=False)
                print(f"Successfully processed table with ID '{id}'")
            except Exception as e:
                print(f"Error processing table with ID '{id}': {e}")

finally:
    # Close the browser
    browser.quit()

# Analysis
# The script successfully extracts and organizes tabular data into an Excel file. 
# Each table represents a unique aspect of property trends in Cape Town City Centre, such as:
# 1. Annual sale and listing trends.
# 2. Total number of properties.
# 3. Average listing price by number of bedrooms.
# 4. Popular sold properties.
# 5. Demographic age profiles of buyers.

# The Excel report can now be used for further exploratory data analysis (EDA) or visualization using tools like Excel, Python, or Power BI.

# Conclusion
# The automation script effectively retrieves structured tabular data from the target website.
# This enables stakeholders to:
# 1. Monitor trends in the Cape Town property market.
# 2. Make data-driven decisions for investments and housing developments.
# 3. Analyze buyer demographics and their preferences.
# Future improvements include adding error handling for intermittent network issues and scheduling periodic data extraction.
