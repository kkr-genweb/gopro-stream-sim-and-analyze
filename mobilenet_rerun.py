# === Client Script to Connect to GoPro Simulator and Detect Objects ===
import cv2
import rerun as rr
import requests
import numpy as np


rr.init("rerun_example_my_data", spawn=True)

# --- Model and Class Configuration ---
# Define the paths to the Caffe model files
prototxt_path = "deploy.prototxt"
model_path = "mobilenet_iter_73000.caffemodel"

# Minimum confidence threshold to filter weak detections
CONFIDENCE_THRESHOLD = 0.5

# List of class labels the MobileNet SSD model was trained to detect.
# The index of the class corresponds to the model's output.
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

# Colors for the bounding boxes (optional, for visual distinction)
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# --- Main Application ---
print("[INFO] Loading model...")
try:
    net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
except cv2.error as e:
    print(f"[ERROR] Could not load model. Ensure '{prototxt_path}' and '{model_path}' are in the same directory.")
    print(f"OpenCV Error: {e}")
    exit()

# Start simulated GoPro stream
print("[INFO] Starting video stream...")

# Connect to the video stream URL
stream_url = 'http://34.0.149.93:8085/video'
cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("[ERROR] Failed to open video stream. Check the URL and server status.")
    exit()

print("[INFO] Processing stream... Press 'q' to quit.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("[WARNING] Failed to get frame, retrying...")
        # Add a small delay before retrying to avoid spamming requests
        cv2.waitKey(500)
        continue

    (h, w) = frame.shape[:2]

    # Pre-process the frame for the neural network
    # 1. Resize to a fixed 300x300 pixels.
    # 2. Normalize the pixel values.
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

    # Pass the blob through the network to get detections
    net.setInput(blob)
    detections = net.forward()

    # Loop over the detections
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        # Filter out weak detections by ensuring the confidence is greater than the threshold
        if confidence > CONFIDENCE_THRESHOLD:
            # Get the class label index and the coordinates of the bounding box
            idx = int(detections[0, 0, i, 1])
            class_label = CLASSES[idx]

            # We only care about 'person' and 'car'
            if class_label in ["person", "car"]:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # Create the label text with the class and confidence
                label = f"{class_label.capitalize()}: {confidence:.2%}"

                # Draw the bounding box and the label on the frame
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                
                # Position the text just above the bounding box
                y = startY - 15 if startY - 15 > 15 else startY + 15
                print(f"[INFO] Detected {label} at [{startX}, {startY}, {endX}, {endY}]")

                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the resulting frame
    #cv2.imshow("Object Detection Stream", frame)
    rr.log("detection", rr.Image(frame))

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
print("[INFO] Cleaning up and stopping stream...")
cap.release()
cv2.destroyAllWindows()
