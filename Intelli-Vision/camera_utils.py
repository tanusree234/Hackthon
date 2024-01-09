import cv2
import time
from picamera2 import Picamera2, Preview
from utils import *
from distance_utils import *
from gps_utils import *
from database_utils import *
import json
import RPi.GPIO as GPIO
from collections import Counter


normalSize = (640, 480)
lowresSize = (320, 240)

picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": normalSize},
                                              lores={"size": lowresSize, "format": "YUV420"})
picam2.configure(config)
stride = picam2.stream_configuration("lores")["stride"]

animals = ['bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe']
electronic_devices = ['tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster']
furniture = ['chair', 'couch', 'bed', 'dining table']
food_and_drinks = ['banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl']
vehicles = ['bicycle', 'motorcycle', 'car', 'airplane', 'bus', 'train', 'truck', 'boat']
traffic = ['traffic light', 'fire hydrant', 'stop sign', 'parking meter']

def capture_and_process():
    try:
        # Set initial random GPS coordinates
        current_latitude, current_longitude = generate_nearby_coordinates()
        distance = generate_random_distance()  # Initial distance (in meters)
        previous_dist = -1

        while True:
            # Video info
            buffer = picam2.capture_buffer("lores")
            grey = buffer[:stride * lowresSize[1]].reshape((lowresSize[1], stride))
            image = cv2.cvtColor(grey, cv2.COLOR_GRAY2RGB)

            # Check internet connectivity
            if check_internet():
                # Send image for prediction using LLM model
                response = send_images_for_prediction(image, distance)
                json_response = json.loads(response)
                alert = json_response['Alert']
                if alert.lower() != "none" and alert != "":
                    text_to_speech(json_response['Description'])
                json_response["Distance"] = distance
                json_response["latitude"] = current_latitude
                json_response["longitude"] = current_longitude
                json_response["Mode"] = "Online"
            else:
                # Get predictions from YOLO model
                response = yolo_prediction(image)
                objects = []
                for box in response.boxes:
                    class_id = response.names[box.cls[0].item()]
                    cords = box.xyxy[0].tolist()
                    cords = [round(x) for x in cords]
                    conf = round(box.conf[0].item(), 2)
                    # print("Object type:", class_id)
                    # print("Coordinates:", cords)
                    # print("Probability:", conf)
                    # print("---")
                    if conf > 0.5:
                        objects.append(class_id)

                print(objects)
                # Use Counter to count occurrences of each item
                item_counts = Counter(objects)
                # Create a string representation
                item_description = ", ".join(
                    f"{item} are {count} {'item' if count == 1 else 'items'}" for item, count in item_counts.items()
                )

                # Count occurrences of "Person"
                person_count = objects.count("person")

                alert_str = ""
                desc_str = ""
                if person_count > 5:
                    alert_str += " |Overcrowded| "
                    desc_str += "Infront of you there is a overcrowded place. "

                if any(item in vehicles for item in objects) and (distance-previous_dist < 0):
                    alert_str += " |Vehicle approaching| "
                    desc_str += f"Vehicle approaching towards you. Currently at a distance of : {distance} meters " 

                if "knife" in objects:
                    alert_str += " |Knife| "
                    desc_str += "person carrying knife towards you. "

                desc_str += item_description
                alert_list = alert_str.split("|")
                alert_list = [a.strip() for a in alert_list if a]
                final_alert_str = ", ".join(alert_list)

                if alert_str:
                    text_to_speech(desc_str)

                json_response = {
                    "Mode": "Offline",
                    "Alert" : final_alert_str,
                    "Description" : desc_str,
                    "Objects": ", ".join(objects),
                    "Distance" : distance,
                    "latitude": current_latitude,
                    "longitude": current_longitude,
                }

            if distance < 20:
                print("distance alert")
            # Save the image and information to the database
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            image_path = f'captured_images/{timestamp}.jpg'  # Change the path as needed
            json_response["Image Path"] = image_path

            print(json_response)
            # Save the captured image with timestamp
            cv2.imwrite(image_path, image)
            save_to_database(json_response)
            previous_dist = distance
            # Wait for 5 seconds before capturing the next image
            time.sleep(5)
            # Update distance for every loop
            distance = update_distance(distance)
            # Generate random GPS coordinates for Hyderabad
            current_latitude, current_longitude = generate_nearby_coordinates()

    except KeyboardInterrupt:
        pass

    finally:
        picam2.stop()
        picam2.stop_preview()
        picam2.close()

if __name__ == "__main__":
    capture_and_process()
