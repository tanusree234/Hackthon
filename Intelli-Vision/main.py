import cv2
import requests
import numpy as np
import time
import serial
import string
import pynmea2
from picamera2 import MappedArray, Picamera2, Preview

normalSize = (640, 480)
lowresSize = (320, 240)

from utils import * 

# Main function
def main():
    picam2 = Picamera2()
    picam2.start_preview(Preview.QTGL)
    config = picam2.create_preview_configuration(main={"size": normalSize},
                                                    lores={"size": lowresSize, "format": "YUV420"})
    picam2.configure(config)

    stride = picam2.stream_configuration("lores")["stride"]
    # picam2.post_callback = DrawRectangles
    picam2.start()

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

        if check_internet(): # 
            # Send image for prediction using LLM model
            response = send_images_for_prediction(image)
            print(response)
            text_to_speech(response)
            # # Get predictions from LLM model
            # predictions = []  # Replace this with actual predictions from LLM model
            # read_predictions(predictions)
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
                # print("Object type:", class_id)
                # print("Coordinates:", cords)
                # print("Probability:", conf)
                # print("---")
                if conf > 0.5:
                    objects.append(class_id)

            print(objects)
            
            template_str = f"Objects infront of you are : " + ", ". join(objects) + ". So be careful"
            print(template_str)
            text_to_speech(template_str)
            # read_predictions(predictions)

        # Wait for 5 seconds before capturing the next image
        time.sleep(5)

if __name__ == "__main__":
    main()
