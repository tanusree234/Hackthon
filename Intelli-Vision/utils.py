import os
import io
import requests
from vertexai.preview.generative_models import (
    FunctionDeclaration,
    GenerativeModel,
    Part,
    Tool,
)
from pathlib import Path
import google.generativeai as genai
import argparse
import os
import cv2
import numpy as np
import tflite_runtime.interpreter as tflite
import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown

from picamera2 import MappedArray, Picamera2, Preview
from ultralytics import YOLO
from PIL import Image
from gtts import gTTS
import os
import tempfile
import playsound
import pyttsx3

os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")

# 1. Configuration
apikey = input("Provide Gemini API key: ")
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
genai.configure(api_key="AIzaSyCqH3g5P8GhTAOmpitc0Q-hu9whEtvd53c")
generation_config = { "temperature": 0.4, "top_p": 1, "top_k": 32, "max_output_tokens": 4096 }

# 2. Initialise Model
LLMmodel = genai.GenerativeModel( model_name="gemini-pro-vision", generation_config=generation_config )
YOLOmodel = YOLO("models/yolov8m.pt")

def to_markdown(text):
    text = text.replace("•", "  *")
    return Markdown(textwrap.indent(text, "> ", predicate=lambda _: True))

def text_to_speech_save_file(text):
    # Create a temporary file to save the generated audio
    temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    
    # Use gTTS to generate audio from text
    tts = gTTS(text=text, lang='en')
    tts.save(temp_audio_file.name)

    # Play the generated audio
    playsound.playsound(temp_audio_file.name, True)

    # Remove the temporary audio file
    os.remove(temp_audio_file.name)

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to check internet connectivity
def check_internet():
    try:
        requests.get("http://www.google.com", timeout=1)
        return True
    except requests.ConnectionError:
        return False

# Function to send images for prediction using LLM model
def send_images_for_prediction(image):
    image_bytes = cv2.imencode('.jpg', image)[1].tobytes()
    
    # Convert bytes to PIL Image
    pil_image = Image.open(io.BytesIO(image_bytes))

    # 3. Generate Content    
    response = LLMmodel.generate_content(
        ["You are blind person assistant becoming their vision. Guide the person about objects/People which are near and if they are very close by then alert the user on the same \n", pil_image]
    )
    response.resolve()

    return response.text
                
# Function to get predictions from YOLO model
def yolo_prediction(image):
    
    results = YOLOmodel.predict(image)
    result = results[0]

    return result




