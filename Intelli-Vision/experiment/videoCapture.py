import cv2
import os
import time

# Constant variables
output_folder = "frames"
capture_interval = 5
num_frames = 10
f_count = 1

# Open the default camera
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get video properties
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Calculate the number of frames to capture
total_frames = int(fps * capture_interval * num_frames)


while f_count <= total_frames:
    # Capture frame-by-frame
    ret, frame = cap.read()
    print(f"fps calculation: {f_count % int(fps * capture_interval)}")
    # If the frame was successfully read
    if ret:
        # Save the current frame into a file
        timestamp = int(time.time())
        filename = f"{output_folder}/frame_{timestamp}.png"
        cv2.imwrite(filename, frame)
        print(f"Frame captured: {filename}")
        f_count += 1

        # Display the resulting frame
        cv2.imshow('Input', frame)
    else:
        break

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture and destroy the windows
cap.release()
cv2.destroyAllWindows()
