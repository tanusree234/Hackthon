import math
import random


# Replace these values with the actual reference location for Hyderabad
latitude = 17.385044  # Hyderabad
longitude = 78.486671

def generate_nearby_coordinates(max_distance=0.05):
    # The max_distance is set to 0.05 (approximately 5.5 km) as an example
    # You can adjust this value based on your requirement
    
    # Convert latitude and longitude from degrees to radians
    lat_rad = math.radians(latitude)
    lon_rad = math.radians(longitude)

    # Earth's radius in kilometers
    earth_radius = 6371.0

    # Generate random distances within max_distance
    distance = max_distance * math.sqrt(random.uniform(0, 1))
    angle = random.uniform(0, 2 * math.pi)

    # Calculate new latitude and longitude
    new_lat = math.degrees(math.asin(math.sin(lat_rad) * math.cos(distance / earth_radius) +
                        math.cos(lat_rad) * math.sin(distance / earth_radius) * math.cos(angle)))
    new_lon = math.degrees(lon_rad + math.atan2(math.sin(angle) * math.sin(distance / earth_radius) * math.cos(lat_rad),
                        math.cos(distance / earth_radius) - math.sin(lat_rad) * math.sin(math.radians(new_lat))))

    return new_lat, new_lon