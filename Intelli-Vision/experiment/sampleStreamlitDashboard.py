import streamlit as st
import cv2
import speech_recognition as sr
from pydub import AudioSegment

# Create the app's title
st.title('Streamlit Dashboard with Voice Input and Video Capture')

# Add a file uploader for the video
uploaded_file = st.file_uploader("Upload a video")
if uploaded_file is not None:
    # Open the video file
    video = cv2.VideoCapture(uploaded_file.name)

    # Display the video frame by frame
    stframe = st.empty()
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        stframe.image(frame[:, :, ::-1])

# Add a file uploader for the audio
uploaded_file = st.file_uploader("Upload an audio file")
if uploaded_file is not None:
    # Convert the audio file to WAV
    audio = AudioSegment.from_file(uploaded_file.name)
    audio.export("audio.wav", format="wav")

    # Use the SpeechRecognition library to convert the audio to text
    r = sr.Recognizer()
    with sr.AudioFile("audio.wav") as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        st.write(text)
