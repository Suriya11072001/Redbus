import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import datetime

# Database connection using SQLAlchemy
# Replace 'username', 'password', 'host', 'port', and 'database' with your actual credentials
host="localhost"
port="5432"
database="Redbusproject"
username="postgres"
password="Suriya"
engine_string = f"postgresql://{username}:{password}@{host}:{port}/{database}"

# Fetch data from the database
query = "SELECT * FROM busdetails1"
data = pd.read_sql(query, engine_string)

# Streamlit app layout
st.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTf4JcPOmb1mHV8pCVeqO7OXce9XiHHRMCq8Q&s',width=200)
   
st.title('Redbus Routes Data Filtering and Analysis')

# Filters
bustype_filter = st.multiselect('Select Bus Type:', options=data['bus_type'].unique())
route_filter = st.multiselect('Select Route:', options=data['route_name'].unique())
price_filter = st.slider('Select Price Range:', min_value=float(data['prices'].min()), max_value=float(data['prices'].max()), value=(float(data['prices'].min()), float(data['prices'].max())))
star_filter = st.slider('Select Star Rating Range:', min_value=float(data['star_ratings'].min()), max_value=float(data['star_ratings'].max()), value=(float(data['star_ratings'].min()), float(data['star_ratings'].max())))
availability_filter = st.slider('Select Seat Availability Range:', min_value=int(data['seats_available'].min()), max_value=int(data['seats_available'].max()), value=(int(data['seats_available'].min()), int(data['seats_available'].max())))


# Filter data based on user inputs

filtered_data = data

if bustype_filter:
    filtered_data = filtered_data[filtered_data['bus_type'].isin(bustype_filter)]

if route_filter:
    filtered_data = filtered_data[filtered_data['route_name'].isin(route_filter)]
filtered_data['prices']=pd.to_numeric(filtered_data['prices'],errors='coerce')
filtered_data.dropna(subset=['prices'],inplace=True)
filtered_data = filtered_data[(filtered_data['prices'] >= price_filter[0]) & (filtered_data['prices'] <= price_filter[1])]
filtered_data = filtered_data[(filtered_data['star_ratings'] >= star_filter[0]) & (filtered_data['star_ratings'] <= star_filter[1])]
filtered_data = filtered_data[(filtered_data['seats_available'] >= availability_filter[0]) & (filtered_data['seats_available']<= availability_filter[1])]


# Display filtered data
st.write('Filtered Data:')
st.dataframe(filtered_data)

# Add a download button to export the filtered data
if not filtered_data.empty:
    st.download_button(
        label="Download Filtered Data",
        data=filtered_data.to_csv(index=False),
        file_name="filtered_data.csv",
        mime="text/csv"
    )

else:
    st.warning("No data available with the selected filters.")