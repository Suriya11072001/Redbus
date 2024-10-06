import pandas as pd
from selenium import webdriver
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
df_Assam_1=pd.read_csv('df_Assam_1.csv')
df_Bsrtc_1=pd.read_csv('df_Bsrtc_1.csv')
df_ctu_1=pd.read_csv('df_ctu_1.csv')
df_ksrtc_1=pd.read_csv('df_ksrtc_1.csv')
df_Nbstc_1=pd.read_csv('df_Nbstc_1.csv')
df_Hrtc_1=pd.read_csv('df_Hrtc_1.csv')
df_pupsu_1=pd.read_csv('df_pupsu_1.csv')
df_Sbstc_1=pd.read_csv('df_Sbstc_1.csv')
df_Tgsrtc_1=pd.read_csv('df_Tgsrtc_1.csv')
df_wbtc_1=pd.read_csv('df_wbtc_1.csv')
dfbus=pd.concat([df_Assam_1,df_Bsrtc_1,df_ctu_1,df_ksrtc_1,df_Nbstc_1,df_Hrtc_1,df_pupsu_1,df_Sbstc_1,df_Tgsrtc_1,df_wbtc_1])

data=pd.read_csv('data3.csv')
data1=pd.DataFrame(data)

#print(data1.isnull().sum())
data2=data['dapartingtime']=pd.to_datetime(data['dapartingtime'],format='%H:%M',errors='coerce').dt.time

print(data2)

#print(data1.info())

# connection=psycopg2.connect(
#      host='localhost',
#      user='postgres',
#      database='Redbusproject',
#      password='Suriya'
#  )
# cursor=connection.cursor()
# cursor.execute("""
#  create table if not exists Busdetails1(
#     id serial PRIMARY KEY,
#     Route_Link TEXT,
#     Route_Name TEXT, 
#     Bus_names TEXT,
#     departingtime time,
#     Total_duration TEXT,
#     Boardingtime time,
#     Star_Ratings decimal,
#     prices float,
#     Seats_available int,
#     Bus_type TEXT)
# """)
# print("table created successfully")
# sql_query = ("""
#          INSERT INTO Busdetails1(
#             Route_Link, Route_Name,Bus_names,departingtime,Total_duration, Boardingtime,
#             Star_Ratings, prices, Seats_available,Bus_type
#         ) VALUES (
#             %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
# """)

# for index,row in data1.iterrows():
#     cursor.execute(sql_query,(row['Route_Link'],row['Route_Name'],row['Bus_names'],row['dapartingtime'],
#                    row['Total_duration'],row['Boardingtime'],row['Star_Ratings'],row['prices'],row['Seats_Available'],row['Bus_typse']))

# connection.commit()

# print("Data has been successfully saved to the database.")

















