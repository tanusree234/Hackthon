import random

def generate_random_distance():
    return round(random.uniform(0, 100), 2)

def update_distance(distance):
    distance -= 2  # Example decrement, adjust as needed
    if distance < 0:
        distance = generate_random_distance()
    return distance
