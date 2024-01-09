import RPi.GPIO as GPIO
import time
import cv2
import requests
import numpy as np
import serial
import string
import pynmea2
from picamera2 import MappedArray, Picamera2, Preview
from utils import *
import math
import random

normalSize = (640, 480)
lowresSize = (320, 240)

# Set GPIO mode and pins
GPIO.setmode(GPIO.BCM)
button_pin = 17
led_pin = 18
buzzer_pin = 27

# Set up GPIO for button, LED, and buzzer
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(buzzer_pin, GPIO.OUT)

# Flag to indicate if the process is running
process_running = False

picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": normalSize},
                                              lores={"size": lowresSize, "format": "YUV420"})
picam2.configure(config)
stride = picam2.stream_configuration("lores")["stride"]

# Database setup (replace with your database configuration)
# You can use any database library (e.g., sqlite3, SQLAlchemy, etc.)
import sqlite3

conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

# Create a table for storing captured images and information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS captured_images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        gps_latitude REAL,
        gps_longitude REAL,
        distance TEXT,
        image_path TEXT,
        response TEXT
    )
''')
conn.commit()

def save_to_database(gps_latitude, gps_longitude, distance, image_path, response):
    cursor.execute('''
        INSERT INTO captured_images (gps_latitude, gps_longitude, distance, image_path, response)
        VALUES (?, ?, ?, ?, ?)
    ''', (gps_latitude, gps_longitude, distance, image_path, response))
    conn.commit()


# Function to generate nearby coordinates
def generate_nearby_coordinates(latitude, longitude, max_distance=0.01):
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


def button_callback(channel):
    global process_running
    if not process_running:
        print("Button pressed! Turning on LED, buzzing the buzzer, and starting camera feed.")
        
        # Turn on LED
        GPIO.output(led_pin, GPIO.HIGH)
        
        # Buzz the buzzer
        GPIO.output(buzzer_pin, GPIO.HIGH)
        time.sleep(1)  # Buzz for 1 second
        GPIO.output(buzzer_pin, GPIO.LOW)
        
        picam2.start_preview(Preview.QTGL)
        # Start camera feed
        picam2.start()

        process_running = True
    else:
        print("Button pressed! Turning off LED, stopping buzzer, and stopping camera feed.")
        
        # Turn off LED
        GPIO.output(led_pin, GPIO.LOW)
        
        # Stop the buzzer
        GPIO.output(buzzer_pin, GPIO.LOW)
        
        # Stop camera feed
        picam2.stop()
        picam2.stop_preview()
        process_running = False

# Add event listener for the button press
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_callback, bouncetime=300)

try:
    print("Waiting for button press...")
    while True:
        # GPS Info
        port = "/dev/ttyAMA0"
        ser = serial.Serial(port, baudrate=9600, timeout=0.5)
        dataout = pynmea2.NMEAStreamReader()
        newdata = ser.readline()

        if newdata[0:6] == "$GPRMC":
            newmsg = pynmea2.parse(newdata)
            lat = newmsg.latitude
            lng = newmsg.longitude
            gps = "Latitude=" + str(lat) + "and Longitude=" + str(lng)
            print(gps)

        # Video info
        buffer = picam2.capture_buffer("lores")
        grey = buffer[:stride * lowresSize[1]].reshape((lowresSize[1], stride))
        image = cv2.cvtColor(grey, cv2.COLOR_GRAY2RGB)

        if check_internet():
            # Send image for prediction using LLM model
            response = send_images_for_prediction(image)
            print(response)

            # Save the image and information to the database
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            image_path = f'captured_images/{timestamp}.jpg'  # Change the path as needed
            save_to_database(lat, lng, "your_distance_info", image_path, response)

            # Save the captured image with timestamp
            cv2.imwrite(image_path, image)
        else:
            print("No internet connection. Hence using the YOLO local model")     
            # Get predictions from YOLO model
            result = yolo_prediction(image)
            
            objects = []
            for box in result.boxes:
                class_id = result.names[box.cls[0].item()]
                cords = box.xyxy[0].tolist()
                cords = [round(x) for x in cords]
                conf = round(box.conf[0].item(), 2)
                if conf > 0.5:
                    objects.append(class_id)

            print(objects)
            
            template_str = f"Objects in front of you are: " + ", ".join(objects) + ". So be careful"
            print(template_str)

            # Save the image and information to the database
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            image_path = f'captured_images/{timestamp}.jpg'  # Change the path as needed
            save_to_database(lat, lng, "your_distance_info", image_path, template_str)

            # Save the captured image with timestamp
            cv2.imwrite(image_path, image)

        # Wait for 5 seconds before capturing the next image
        time.sleep(5)

except KeyboardInterrupt:
    pass

finally:
    # Cleanup GPIO and close the camera
    GPIO.cleanup()
    picam2.stop()
    picam2.close()
    conn.close()
