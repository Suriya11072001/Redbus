#importing libraries
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Read the CSV
df_Ksrtc = pd.read_csv('df_Kerala.csv')
print(df_Ksrtc)

# Initialize the WebDriver
driver = webdriver.Chrome()
driver.maximize_window()

# Create empty lists
Route_Links = []
Routes_Names = []
Bus_names_list = []
Departingtime_list = []
Total_Duration_list = []
Boardingtime_list = []
star_Ratings_list = []
Prices_list = []
Seats_Available_list = []
Bus_types_list = []

# Loop through each route
for i, r in df_Ksrtc.iterrows():
    links = r["Route_link"]
    routes = r["Route_name"]
    driver.get(links)
    time.sleep(3)

    # Try clicking "View Buses" if button is available
    try:
        view_buses_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'button')]"))
        )
        view_buses_button.click()
        print(f"'View Buses' clicked for route: {routes}")
        time.sleep(5)
    except Exception as e:
        print(f"No 'View Buses' button for route: {routes}, proceeding...")

    # Wait for buses to appear
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'travels')]"))
        )
    except Exception as e:
        print(f"No buses found for route: {routes}")
        continue

    # Scroll to load all buses
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Now scrape data
   # Now scrape data
    bus_name_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'travels')]")
    bustype_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'bus-type')]")
    dptime_elements = driver.find_elements(By.CLASS_NAME, "dp-time.f-19.d-color.f-bold")
    bptime_elements = driver.find_elements(By.CLASS_NAME, "bp-time.f-19.d-color.disp-Inline") 
    dur_elements = driver.find_elements(By.CLASS_NAME, "dur.l-color.lh-24")
    rating_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'rating-sec')]")
    price_elements = driver.find_elements(By.XPATH, '//*[@class="fare d-block"]')
    seats_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'seat-left')]")
    buses_count = len(bus_name_elements)

    # Append data safely
    for j in range(buses_count):
        Route_Links.append(links)
        Routes_Names.append(routes)
        Bus_names_list.append(bus_name_elements[j].text if j < len(bus_name_elements) else '')
        Departingtime_list.append(dptime_elements[j].text if j < len(dptime_elements) else '')
        Total_Duration_list.append(dur_elements[j].text if j < len(dur_elements) else '')
        Boardingtime_list.append(bptime_elements[j].text if j < len(bptime_elements) else '')
        star_Ratings_list.append(rating_elements[j].text if j < len(rating_elements) else '')
        Prices_list.append(price_elements[j].text if j < len(price_elements) else '')
        Seats_Available_list.append(seats_elements[j].text if j < len(seats_elements) else '')
        Bus_types_list.append(bustype_elements[j].text if j < len(bustype_elements) else '')

print("✅ Scraping Successfully Completed!")

# Create final DataFrame
bus_details = {
    'Route_Link': Route_Links,
    'Route_Name': Routes_Names,
    'Bus_names': Bus_names_list,
    'Departingtime': Departingtime_list,
    'Total_duration': Total_Duration_list,
    'Boardingtime': Boardingtime_list,
    'Star_Ratings': star_Ratings_list,
    'Prices': Prices_list,
    'Seats_Available': Seats_Available_list,
    'Bus_type': Bus_types_list,
}

df_Ksrtc_1 = pd.DataFrame(bus_details)

# Save the DataFrame
df_Ksrtc_1.to_csv("df_Ksrtc_1.csv", index=False)
print(df_Ksrtc_1)
