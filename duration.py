import cv2

# Load the video
cap = cv2.VideoCapture("vdo/2.mp4")

# Get frame count and FPS
frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps = cap.get(cv2.CAP_PROP_FPS)

# Calculate duration in seconds
duration = frame_count / fps

# Print the duration
print("Duration of the video:", round(duration), "seconds")

# Release the video capture object
cap.release()