import json
import geocoder
import pyttsx3
import requests


def get_closest_landmark(latitude, longitude, api_key, landmark_type):
    # Define the base URL for the Google Places API
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    # Define the parameters for the API request
    params = {
        "location": f"{latitude},{longitude}",
        "radius": 500,  # Search within a 500 meter radius
        "type": landmark_type,  # We're looking for landmarks
        "key": api_key
    }

    # Send the GET request to the Google Places API
    response = requests.get(base_url, params=params)

    # Parse the response JSON
    response_json = json.loads(response.text)

    # Get the first result from the response
    first_result = response_json["results"][0]

    # Return the name of the first result
    return first_result["name"]


# Geocoding of current location
g = geocoder.ip('me')

# Extract Geocode result
loc = g.latlng

# Replace with your actual latitude, longitude, and API key
lat = loc[0]
lng = loc[1]
api_key = ""
landmark_type = "school"

landmark = get_closest_landmark(lat, lng, api_key, landmark_type)
print(f"The closest {landmark_type} is: {landmark}")
engine = pyttsx3.init()
engine.say(f"The closest {landmark_type} is: {landmark}")
engine.runAndWait()
