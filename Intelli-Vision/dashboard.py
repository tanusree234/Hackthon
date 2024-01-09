import streamlit as st
import pandas as pd
import geocoder
import json
import requests
import pyttsx3
import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access the API key using the environment variable
api_key="AIzaSyCyyYEMD9w13RkHRfylHEjbzliCDfxoWuw"
#api_key = os.getenv("MAP_API_KEY")


# Function to get the closest landmark
def get_closest_landmark(latitude, longitude, api_key, landmark_type):
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{latitude},{longitude}",
        "radius": 500,  # Search within a 500-meter radius
        "type": landmark_type,
        "key": api_key
    }
    response = requests.get(base_url, params=params)
    response_json = json.loads(response.text)

    if response_json.get("results"):
        return response_json["results"][0]["name"]
    else:
        return None


# Function to create a Streamlit dashboard
def main():
    st.set_page_config(layout="wide")
    st.title("Intelli-Vision Dashboard")
    st.sidebar.header("Landmark Detection")

    # Get current location
    g = geocoder.ip('me')
    loc = g.latlng
    lat, lng = loc[0], loc[1]

    # # Replace with your actual Google Maps API key
    # api_key = "YOUR_GOOGLE_MAPS_API_KEY"

    # Landmark types for dropdown
    landmark_types = ["current location", "school", "hospital", "restaurant", "park", "airport", "shop"
                      "gym", "shopping_mall", "movie_theater", "lodging", "museum"]

    # Dropdown for selecting landmark type
    selected_landmark_type = st.sidebar.selectbox("Select Landmark Type", landmark_types)

    # Get the closest landmark
    closest_landmark = get_closest_landmark(lat, lng, api_key, selected_landmark_type)

    # Display the selected landmark
    if closest_landmark:
        st.sidebar.info(f"The closest {selected_landmark_type} is: {closest_landmark}")
        engine = pyttsx3.init()
        engine.say(f"The closest {selected_landmark_type} is: {closest_landmark}")
        engine.runAndWait()
    else:
        st.sidebar.warning("No landmark found.")

    # Display map of the last location
    st.subheader("Map of Last Location")
    st.map(pd.DataFrame({"latitude": [lat], "longitude": [lng]}))

    # Fetch data from the SQLite database
    conn = sqlite3.connect('guidinglight.db')
    query = "SELECT * FROM guidinglight ORDER BY id DESC"
    events_df = pd.read_sql_query(query, conn)
    conn.close()

    # Display events table
    st.subheader("Events Table")
    st.table(events_df)


if __name__ == "__main__":
    main()
