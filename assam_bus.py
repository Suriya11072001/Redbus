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

df_Assam=pd.read_csv('df_Assam.csv')
print(df_Assam)
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

for i,r in df_Assam.iterrows():
    links=r["Route_link"]
    routes=r["Route_name"]
    driver.get(links)
    time.sleep(5)
    elements = driver.find_elements(By.XPATH, f"//a[contains(@href, '{links}')]")
    for element in elements:
        element.click()
        time.sleep(6)
    try:
       view_buses=driver.find_element(By.XPATH,'//div[@class="button"]')
       view_buses.click()
    except:
        continue
    time.sleep(10)       

    
    last_height=driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(5)
        new_height=driver.execute_script("return document.body.scrollHeight")
        if new_height==last_height:
            break
        last_height=new_height
    

#extract bus details
    bus_names = driver.find_elements(By.XPATH, "//div[@class='travels lh-24 f-bold d-color']")   #each row with each index is iterated using the XPATH, 
    bustype = driver.find_elements(By.XPATH, "//div[@class='bus-type f-12 m-top-16 l-color evBus']")  
    dptime = driver.find_elements(By.XPATH, "//*[@class='dp-time f-19 d-color f-bold']")
    bptime= driver.find_elements(By.XPATH, "//*[@class='bp-time f-19 d-color disp-Inline']")
    dur= driver.find_elements(By.XPATH, "//*[@class='dur l-color lh-24']")
    
    #price= driver.find_elements(By.XPATH, '//div[@class="fare d-block"]//span')
    #seat= driver.find_elements(By.XPATH, "//div[contains(@class, 'seat-left')]")

    try:
        rating = driver.find_elements(By.XPATH,"//div[@class='clearfix row-one']/div[@class='column-six p-right-10 w-10 fl']")
    except:
        continue
    price = driver.find_elements(By.XPATH, '//*[@class="fare d-block"]')
    seats = driver.find_elements(By.XPATH, "//div[contains(@class, 'seat-left')]")
    
 # Append data to respective lists
    for bus in bus_names:
        Route_Links.append(links)
        Routes_Names.append(routes)
        Bus_names.append(bus.text)
    for start_time in bptime:
        Departingtime.append(start_time.text)
    for duration in dur:
        Total_Duration.append(duration.text)
    for end_time in bptime:
        Boardingtime.append(end_time.text)
    for ratings in rating:
        star_Ratings.append(ratings.text)
    for ticket_price in price:
        Prices.append(ticket_price.text)
    for seats in seats:
        Seats_Available.append(seats.text)
    for bus_type in bustype:
        Bus_types.append(bus_type.text)
        
print("succesfully completed")
bus_details = {
    'Route_Link':Route_Links,
    'Route_Name':Routes_Names,
    'Bus_names':Bus_names, 
    'dapartingtime':Departingtime, 
    'Total_duration':Total_Duration,
    'Boardingtime':Boardingtime,
    'Star_Ratings':star_Ratings,
    'prices':Prices,
    'Seats_Available':Seats_Available,
    'Bus_typse':Bus_types,
}
df_Assam_1=pd.DataFrame(bus_details)
df_Assam_1.to_csv("df_Assam_1.csv",index=False)
print(df_Assam_1)