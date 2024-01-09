import cv2
import numpy as np


# Define a function to detect walkable roads
def detect_walkable_roads(image_path):

    # Loading image from source path
    img_frame = cv2.imread(image_path)

    # Convert the frame to grayscale
    gray = cv2.cvtColor(img_frame, cv2.COLOR_BGR2GRAY)

    # Apply a Gaussian blur to the grayscale frame
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply a Canny edge detector to the blurred frame
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour
    max_area = 0
    max_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            max_contour = contour

    # Draw the largest contour on the image
    cv2.drawContours(img_frame, [max_contour], 0, (0, 255, 0), 2)

    # Show the image
    cv2.imshow('Image', img_frame)

    # Saving image
    cv2.imwrite(r'C:\Users\tanus\Documents\Github-gl\Hackthon\Intelli-Vision\frames\processed\withline.jpeg'
                , img_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Find the Hough lines in the edge detected frame
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)

    # Filter the Hough lines to find only the walkable roads
    walkable_roads = []
    for line in lines:
        (x1, y1, x2, y2) = line[0]
        if abs(y2 - y1) < 10:
            walkable_roads.append(line)

    # Draw the walkable roads on the frame
    for line in walkable_roads:
        (x1, y1, x2, y2) = line[0]
        cv2.line(img_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return img_frame


frame = r"C:\Users\tanus\Documents\Github-gl\Hackthon\Intelli-Vision\frames\Pic3.jpeg"
# Detect the walkable roads in the frame
final_frame = detect_walkable_roads(frame)

# Display the frame
cv2.imshow('Walkable Roads', final_frame)

# Saving image
cv2.imwrite(r'C:\Users\tanus\Documents\Github-gl\Hackthon\Intelli-Vision\frames\processed\Pic3_processed.jpeg'
            , final_frame)
