import cv2
import requests
import numpy as np

# --- Model and Class Configuration ---
prototxt_path = "deploy.prototxt"
model_path = "mobilenet_iter_73000.caffemodel"
CONFIDENCE_THRESHOLD = 0.5

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# Load model
print("[INFO] Loading model...")
try:
    net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
except cv2.error as e:
    print(f"[ERROR] Could not load model: {e}")
    exit()

# Connect to Pixel stream
stream_url = "http://192.168.1.147:4747/video"
cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("[ERROR] Could not open video stream. Check IP/Webcam app.")
    exit()

print("[INFO] Processing stream... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("[WARNING] Frame grab failed. Retrying...")
        cv2.waitKey(500)
        continue

    (h, w) = frame.shape[:2]

    # Prepare input blob and perform forward pass
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    # Analyze detections
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > CONFIDENCE_THRESHOLD:
            idx = int(detections[0, 0, i, 1])
            class_label = CLASSES[idx]

            if class_label in ["person", "car"]:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                label = f"{class_label.capitalize()}: {confidence:.2%}"

                cv2.rectangle(frame, (startX, startY), (endX, endY),
                              COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                print(f"[INFO] Detected {label} at [{startX}, {startY}, {endX}, {endY}]")
                cv2.putText(frame, label, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

    # Display frame
    cv2.imshow("Object Detection Stream", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("[INFO] Exiting...")
cap.release()
cv2.destroyAllWindows()