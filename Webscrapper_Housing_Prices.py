# importing libraries and webdriver
from selenium import webdriver 
from selenium.webdriver.common.by import By
import pandas as pd

#open web browser using get function
p24_url = 'https://www.property24.com/cape-town/cape-town-city-centre/property-trends/9138'
browser= webdriver.Chrome()
browser.get(p24_url)

#assign tables in listing  
ids = [
        'annualSaleAndListingTrendsGraph',
        'totalNumberOfPropertiesTable',
        'averageListPriceVsBedroomsGraph',
        'soldPropertiesGraph_Popular1',
        'soldPropertiesGraph_Popular2',
        'ageProfileGraph'
    ]

def divide_chunks(l, n):
     
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

with pd.ExcelWriter('output.xlsx', engine='xlsxwriter') as writer:
    for id in ids:
        # get the specified element
        elements = browser.find_elements(By.XPATH, f'//*[@id="{id}"]//table//tr')
        
        columns = list(map(lambda elment: elment.get_attribute("textContent"), browser.find_elements(By.XPATH,f'//*[@id="{id}"]//table//thead//tr//th')))
                
        rows = list(map(lambda elment: elment.get_attribute("textContent"), browser.find_elements(By.XPATH, f'//*[@id="{id}"]//table//tbody//tr//td')))

        pd.DataFrame(divide_chunks(rows, len(columns)), columns=columns).to_excel(writer, sheet_name=id)

# Close the WebDriver object
browser.quit()


