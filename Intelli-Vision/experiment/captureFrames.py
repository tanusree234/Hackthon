import os
import cv2
import time


def capture_and_save_frames(camera_index=1, output_folder="frames", capture_interval=5, num_frames=10
):
    # Open the video capture object
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Calculate the number of frames to capture
    total_frames = int(fps * capture_interval * num_frames)

    # frame counter
    f_count = 1

    # Capture and save frames
    while f_count <= total_frames:
        ret, frame = cap.read()
        time.sleep(1)
        if not ret:
            print("Failed to capture frame")
            break
        print(f"fps calculation: {f_count % int(fps * capture_interval)}")
        # Save frame every capture_interval seconds
        if f_count % int(fps * capture_interval) == 0:
            timestamp = int(time.time())
            filename = f"{output_folder}/frame_{timestamp}.png"  # f"{output_folder}/frame_{i // int(fps * capture_interval)}.jpg"
            cv2.imshow(filename)
            cv2.imwrite(filename, frame)
            print(f"Frame captured: {filename}")

        f_count += 1
        # Wait for a short duration to achieve the desired capture interval
        time.sleep(1 / fps)

    # Release the video capture object
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    capture_and_save_frames(camera_index=0)