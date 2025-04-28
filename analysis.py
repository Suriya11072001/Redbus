import pandas as pd
from selenium import webdriver
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
df_apsrtc_1=pd.read_csv('df_apsrtc_1.csv')
df_Assam_1=pd.read_csv('df_Assam_1.csv')
df_Bsrtc_1=pd.read_csv('df_Bsrtc_1.csv')
df_ctu_1=pd.read_csv('df_ctu_1.csv')
df_ksrtc_1=pd.read_csv('df_ksrtc_1.csv')
df_Nbstc_1=pd.read_csv('df_Nbstc_1.csv')
df_Hrtc_1=pd.read_csv('df_Hrtc_1.csv')
df_Sbstc_1=pd.read_csv('df_Sbstc_1.csv')
df_Tgsrtc_1=pd.read_csv('df_Tgsrtc_1.csv')
df_wbtc_1=pd.read_csv('df_wbtc_1.csv')
dfbus=pd.concat([df_apsrtc_1,df_Assam_1,df_Bsrtc_1,df_ctu_1,df_ksrtc_1,df_Nbstc_1,df_Hrtc_1,df_Sbstc_1,df_Tgsrtc_1,df_wbtc_1])

#drop multiple columns at once
dfbus = dfbus.drop(columns=['prices', 'Bus_typse','dapartingtime'])

# Step 1: Remove rows with any NULL values
dfbus = dfbus.dropna()
# Step 2: Remove duplicate rows
dfbus = dfbus.drop_duplicates()
dfbus['Star_Ratings'] = dfbus['Star_Ratings'].replace("New", 3.5)
# Remove 'INR' and any spaces from the 'prices' column
dfbus['Prices'] = dfbus['Prices'].str.replace('INR', '', regex=False).str.strip()

import re

# # # Keep only digits
dfbus['Seats_Available'] = dfbus['Seats_Available'].apply(lambda x: re.sub(r'\D', '', str(x)))
dfbus['Seats_Available'] = pd.to_numeric(dfbus['Seats_Available'], errors='coerce')


# # Save
dfbus.to_csv('merged_states.csv', index=False)

print("Merged successfully!")


#print(data1.isnull().sum())



#print(data1.info())
# connection with postgresql
connection=psycopg2.connect(
     host='localhost',
     user='postgres',
     database='Redbusproject',
     password='Suriyass'
 )
#create a table schema
cursor=connection.cursor()
cursor.execute("""
 create table if not exists Busdetails1(
    id serial PRIMARY KEY,
    Route_Link TEXT,
    Route_Name TEXT, 
    Bus_names TEXT,
    departingtime time,
    Total_duration TEXT,
    Boardingtime time,
    Star_Ratings decimal,
    prices float,
    Seats_available int,
    Bus_type TEXT)
""")
#print if table is created
print("table created successfully")
#insert the value by using the placeholder
sql_query = ("""
         INSERT INTO Busdetails1(
            Route_Link, Route_Name,Bus_names,Departingtime,Total_duration, Boardingtime,
            Star_Ratings, prices, Seats_available,Bus_type
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""")
# Iterate over DataFrame rows

for index,row in dfbus.iterrows():
 # Execute the query with parameters
    cursor.execute(sql_query,(row['Route_Link'],row['Route_Name'],row['Bus_names'],row['Departingtime'],
                   row['Total_duration'],row['Boardingtime'],row['Star_Ratings'],row['Prices'],row['Seats_Available'],row['Bus_type']))

connection.commit()

print("Data has been successfully saved to the database.")

















