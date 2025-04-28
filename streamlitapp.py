import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import datetime

# App layout config
st.set_page_config(page_title="🚌 Redbus App", layout="wide")

# Custom page background color
# Custom CSS for light red background and styling
st.markdown("""
    <style>
        .stApp {
            background-color: #fff0f0;
        }
        .css-18e3th9 {
            background-color: #fff0f0 !important;
        }
        .css-1d391kg {
            background-color: #fff0f0 !important;
        }
        .stSidebar {
            background-color: #ffe6e6;
        }
        .stButton>button {
            color: white;
            background-color: #e63946;
        }
        h1, h2, h3 {
            color: #b80000;
        }
    </style>
""", unsafe_allow_html=True)

# Database connection using SQLAlchemy
# Replace 'username', 'password', 'host', 'port', and 'database' with your actual credentials
host="localhost"
port="5432"
database="Redbusproject"
username="postgres"
password="Suriyass"
@st.cache_data
def load_data():
    engine_string = f"postgresql://{username}:{password}@{host}:{port}/{database}"
    engine = create_engine(engine_string)

    
    query = "SELECT * FROM busdetails1"
    df = pd.read_sql(query, con=engine)
    engine.dispose()
    return df

# Step 3: Load data
df = load_data()



# Sidebar Navigation
page = st.sidebar.radio("Go to", ["🏠 Home", "📊 Bus Filtering"])

# ================================
# 🏠 HOME PAGE
# ================================
if page == "🏠 Home":
    st.title("🚌 Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit")
    st.markdown("---")

    st.header("📌 Overview")
    st.markdown("""
    This project focuses on scraping real-time bus details from the **Redbus** website, including:
    - Bus names, types, prices
    - Departure & boarding times
    - Duration, seat availability, and ratings

    The scraped data is stored in a **PostgreSQL** database and visualized through an interactive **Streamlit** dashboard.
    """)

    st.header("🎯 Objective")
    st.markdown("""
    - Automate extraction of bus details for selected city routes  
    - Store data in a structured SQL format  
    - Enable easy filtering, searching, and comparison of buses using an intuitive web interface
    """)

    st.header("🛠️ Tools & Technologies Used")
    st.markdown("""
    - **Python**: Core scripting and backend logic  
    - **Selenium**: For browser automation and scraping Redbus website  
    - **PostgreSQL + SQLAlchemy**: For structured storage of data  
    - **Streamlit**: To build an interactive dashboard for users  
    - **Pandas**: For data manipulation and filtering  
    """)

    st.header("✅ Conclusion")
    st.markdown("""
    This project successfully bridges data scraping and web app visualization.  
    The application helps users:
    - View real-time bus listings
    - Apply filters like price, ratings, and timings
    - Make informed decisions based on comprehensive bus data.

    🚀 Ready to explore? Go to the **📊 Bus Filtering** page from the sidebar.
    """)

elif page == "📊 Bus Filtering":
    st.title("📊 Explore and Filter Redbus Details")
    # Filter: Route Name
    route_names = sorted(df['route_name'].unique())
    selected_route = st.sidebar.selectbox("Route Name", route_names)

   
   # ✅ Bus Names Multiselect (user must choose)
    bus_names = sorted(df['bus_names'].dropna().unique())
    selected_bus_names = st.sidebar.multiselect("Bus Names", bus_names)

   # ✅ Bus Types Multiselect (user must choose)
    bus_types = sorted(df['bus_type'].dropna().unique())
    selected_bus_types = st.sidebar.multiselect("Bus Types", bus_types)

    
  # Price Range Radio
    price_option = st.sidebar.radio(
    "Select Price Range (₹)",
    ("All", "50- 1500", "1500 - 2500", "2500 - 3500", "3500 and Above")
)
 
    # Seat Availability Filter
    min_seats = int(df['seats_available'].min())
    max_seats = int(df['seats_available'].max())
    seat_count = st.sidebar.slider("Minimum Seats Available", min_seats, max_seats, min_seats)
    # Apply Filters
    filtered_df = df[
        (df['route_name']==selected_route)&
        (df['bus_names'].isin(selected_bus_names)) &
        (df['bus_type'].isin(selected_bus_types)) &
        (df['seats_available'] >= seat_count)
        
    ]
    # Apply Price Range Filter
    if price_option == "50 - 1500":
        filtered_df = filtered_df[(filtered_df['prices'] >= 50) & (filtered_df['prices'] <= 1500)]
    elif price_option == "1600 - 2500":
        filtered_df = filtered_df[(filtered_df['prices'] >= 1600) & (filtered_df['prices'] <= 2500)]
    elif price_option == "2600 - 3000":
        filtered_df = filtered_df[(filtered_df['prices'] >= 2600) & (filtered_df['prices'] <= 3000)]
    elif price_option == "3000 and Above":
        filtered_df = filtered_df[(filtered_df['prices'] > 3000)]
    # Display Filtered Results
    st.markdown(f"### Showing {len(filtered_df)} result(s)")
    st.dataframe(filtered_df, use_container_width=True)
    
