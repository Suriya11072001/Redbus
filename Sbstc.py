# Importing libraries
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Initialize the web driver
driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://www.redbus.in/online-booking/south-bengal-state-transport-corporation-sbstc/?utm_source=rtchometile')
time.sleep(5)

def Sbstc_link_route(Sbstc):
    Links_Sbstc= []
    Routes_Sbstc = []

    # Function to collect route data from the current page
    def collect_routes():
        routes = driver.find_elements(By.CLASS_NAME, 'route')
        for routes_links in routes:
            route_link = routes_links.get_attribute('href')
            Links_Sbstc.append(route_link)
            Routes_Sbstc.append(routes_links.text)

    # Collect data from the first page
    collect_routes()

    # Handling pagination for the next pages
    for page_number in range(1, 6):  # Page 2 and onwards
        if page_number<5:
           try:
              pagination_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="DC_117_paginationTable"]')))

            # Locate the next page button
              next_page_button = pagination_container.find_element(By.XPATH, f'//div[contains(@class, "DC_117_pageTabs") and text()="{page_number + 1}"]')

              actions = ActionChains(driver)
              actions.move_to_element(next_page_button).perform()
              time.sleep(3)

              print(f"Clicking on page {page_number + 1}")

              next_page_button.click()

            # Wait until the new page is loaded
              WebDriverWait(driver, 10).until(
                EC.text_to_be_present_in_element(
                    (By.XPATH, '//div[contains(@class, "DC_117_pageTabs DC_117_pageActive")]'),str(page_number + 1)))
                
            
            
              print(f"Successfully navigated to page {page_number + 1}")

            # After page navigation, collect the data for the current page
              time.sleep(3)  # Wait for data to load
              collect_routes()  # Collect data from the current page

           except Exception as e:
              print(f"An error occurred while navigating to page {page_number + 1}: {e}")
              break

    return Links_Sbstc, Routes_Sbstc

# Call the function
Links_Sbstc, Routes_Sbstc= Sbstc_link_route('Sbstc')

# Quit the driver after scraping
driver.quit()

# Save data to a CSV file
df_Sbstc = pd.DataFrame({"Route_name": Routes_Sbstc, "Route_link": Links_Sbstc})
df_Sbstc.to_csv("df_Sbstc.csv", index=False)

# Print the dataframe
print(df_Sbstc)