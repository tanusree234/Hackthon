import streamlit as st
import threading
import pyaudio
import wave
import cv2
import os
import time
from datetime import datetime

APP_TITLE = "Smart Eye"
APP_SUB_TITLE = "Enhancing Capabilities with GenAI and IoT Integration"

# Create a directory to store the captured frames
import streamlit as st
import cv2
import numpy as np
import time
import threading
import os
import pyaudio
import wave

APP_TITLE = "Your App Title"
APP_SUB_TITLE = "Your App Subtitle"

# Create a directory to store the captured frames
frames_directory = "captured/frames"
audio_directory = "captured/audio"
processing_dir = os.path.join(frames_directory, "processing")
processed_dir = os.path.join(frames_directory, "processed")

# Constants for audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024

if not os.path.exists(frames_directory):
    os.makedirs(frames_directory)

if not os.path.exists(audio_directory):
    os.makedirs(audio_directory)


def capture_audio(filename, duration, timestamp):
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    frames = []

    while time.time() - timestamp < duration:
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the audio file with a timestamp in the filename
    timestamped_filename = f"{filename}_{timestamp}.wav"

    with wave.open(timestamped_filename, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))

    return timestamped_filename


def capture_and_store_frames(
    camera_index=0,
    frames_directory="captured_frames",
    source_name="source1",
    capture_interval=5,
    num_frames=10,
):
    # Create a VideoCapture object
    cap = cv2.VideoCapture(camera_index)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Create a unique id for the HTML element
    image_id = f"video_frame_{source_name}"
    st.session_state[image_id] = None  # Initialize session state for the image

    try:
        for i in range(num_frames):
            timestamp = int(time.time())  # Common timestamp for both image and audio

            # Capture a frame
            ret, frame = cap.read()

            if not ret:
                print("Failed to capture frame")
                break

            # Save frame every capture_interval seconds
            filename = f"{frames_directory}/{source_name}_frame_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Frame captured: {filename}")

            # Audio capture
            audio_filename = f"{source_name}"
            audio_capture_duration = capture_interval

            audio_thread = threading.Thread(
                target=capture_audio,
                args=(audio_filename, audio_capture_duration, timestamp),
            )
            audio_thread.start()

            # Update the number of images captured
            st.session_state[image_id] = frame  # Store the frame in session state

            # Wait for the specified capture interval
            time.sleep(capture_interval)

    except KeyboardInterrupt:
        pass
    finally:
        # Release the video capture object
        cap.release()


def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    if "capturing" not in st.session_state:
        st.session_state.capturing = False

    if st.sidebar.toggle("Live?"):
        container_2 = st.empty()
        button_A = container_2.button("Start Capturing")

        if button_A:
            container_2.empty()
            button_B = container_2.button("Capturing... (Click to Stop)")

            if button_B:
                container_2.empty()
                button_A = container_2.button("Start Capturing")
            else:
                st.warning("Capturing frames... Press the button again to stop.")

                # Audio capture setup
                audio_filename = "captured_audio"
                audio_capture_duration = 5  # Adjust as needed

                audio_thread = threading.Thread(
                    target=capture_audio,
                    args=(audio_filename, audio_capture_duration),
                )
                audio_thread.start()

                # Capture frames for source1
                capture_and_store_frames(source_name="source1")

                # Capture frames for source2
                capture_and_store_frames(source_name="source2")

                # Additional logic related to the "Capturing... (Click to Stop)" button can be placed here
            # Remove the audio_thread.join() line

        # Display the frames in the main area
        if st.session_state.get("video_frame_source1"):
            st.image(st.session_state["video_frame_source1"], caption="Source 1")

        if st.session_state.get("video_frame_source2"):
            st.image(st.session_state["video_frame_source2"], caption="Source 2")

    else:
        vid_source1 = st.sidebar.file_uploader(
            "Recorded Video (Source 1)", type="video/mp4"
        )
        if vid_source1:
            st.video(vid_source1, format="video/mp4", start_time=0)

        vid_source2 = st.sidebar.file_uploader(
            "Recorded Video (Source 2)", type="video/mp4"
        )
        if vid_source2:
            st.video(vid_source2, format="video/mp4", start_time=0)

    if st.sidebar.button("Add Custom Source"):
        uploaded_file = st.sidebar.file_uploader(
            "Upload a video file", type=["mp4", "avi", "mkv"]
        )
        if uploaded_file is not None:
            st.video(uploaded_file)


if __name__ == "__main__":
    main()
