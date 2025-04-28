#importing libraries
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
# read the csv file
df_ctc=pd.read_csv('df_ctu.csv')
print(df_ctc)
#initialize the web driver
driver=webdriver.Chrome()
driver.maximize_window()

Route_Links= []
Routes_Names = []
Bus_names = []
Departingtime= []
Total_Duration= []
Boardingtime= []
star_Ratings = []
Prices= []
Seats_Available= []
Bus_types= []

for i, r in df_ctc.iterrows():
    links = r["Route_link"]
    routes = r["Route_name"]
    driver.get(links)
    
    try:
        # Wait until bus list is present
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'travels')]"))
        )
    except Exception as e:
        print(f"Failed to load page {links}: {e}")
        continue
    
    time.sleep(5)  # give extra time just in case
    
    # Scroll page fully
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Now scrape data
    bus_name_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'travels')]")
    bustype_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'bus-type')]")
    dptime_elements = driver.find_elements(By.CLASS_NAME, "dp-time.f-19.d-color.f-bold")
    bptime_elements = driver.find_elements(By.CLASS_NAME, "bp-time.f-19.d-color.disp-Inline") 
    dur_elements = driver.find_elements(By.CLASS_NAME, "dur.l-color.lh-24")
    rating_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'rating-sec')]")
    price_elements = driver.find_elements(By.XPATH, '//*[@class="fare d-block"]')
    seats_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'seat-left')]")
    
    buses_count = len(bus_name_elements)  # total buses found

    for j in range(buses_count):
        Route_Links.append(links)
        Routes_Names.append(routes)
        Bus_names.append(bus_name_elements[j].text if j < len(bus_name_elements) else '')
        Departingtime.append(dptime_elements[j].text if j < len(dptime_elements) else '')
        Total_Duration.append(dur_elements[j].text if j < len(dur_elements) else '')
        Boardingtime.append(bptime_elements[j].text if j < len(bptime_elements) else '')
        star_Ratings.append(rating_elements[j].text if j < len(rating_elements) else '')
        Prices.append(price_elements[j].text if j < len(price_elements) else '')
        Seats_Available.append(seats_elements[j].text if j < len(seats_elements) else '')
        Bus_types.append(bustype_elements[j].text if j < len(bustype_elements) else '')

print("Successfully completed scraping!")

# Create DataFrame
bus_details = {
    'Route_Link': Route_Links,
    'Route_Name': Routes_Names,
    'Bus_names': Bus_names,
    'Departingtime': Departingtime,
    'Total_duration': Total_Duration,
    'Boardingtime': Boardingtime,
    'Star_Ratings': star_Ratings,
    'Prices': Prices,
    'Seats_Available': Seats_Available,
    'Bus_type': Bus_types,
}
df_ctc_1 = pd.DataFrame(bus_details)
df_ctc_1.to_csv("df_ctc_1.csv", index=False)
print(df_ctc_1)
