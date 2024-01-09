import googlemaps
from datetime import datetime
import geocoder
import math


def calculate_footsteps(source, destination):
    """Calculates the footsteps from a source to a destination.

  Args:
    source: The source coordinates.
    destination: The destination coordinates.

  Returns:
    A list of footsteps.
  """

    # Calculate the distance between the source and destination.
    distance = math.sqrt((destination[0] - source[0]) ** 2 + (destination[1] - source[1]) ** 2)

    # Calculate the number of footsteps needed to travel the distance.
    foot_steps = int(distance / 2)

    # Create a list of footsteps.
    footsteps_list = []
    for i in range(foot_steps):
        footsteps_list.append((source[0] + i, source[1]))

    return footsteps_list


gmaps = googlemaps.Client(key='AIzaSyCyyYEMD9w13RkHRfylHEjbzliCDfxoWuw')

g = geocoder.ip('me')
print(g.latlng)
print(g)
print(f"Calculate foot steps : {calculate_footsteps(g.latlng, [18.5151946, 73.9214669])}")


# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode(tuple(g.latlng))
print(f"reverse geo code: {reverse_geocode_result}")

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions(origin="Kiarah Terrazo",
                                     destination="Magarpatta West Gate",
                                     mode="transit",
                                     departure_time=now)
print(f"Direction result: {directions_result}")
# Validate an address with address validation
addressvalidation_result = gmaps.addressvalidation(["Magarpatta West Gate", ],
                                                   regionCode='India',
                                                   locality='Pune',
                                                   enableUspsCass=True)
