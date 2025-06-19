# GoPro Video Processing and Object Detection

This repository contains a collection of Python scripts for working with GoPro camera streams, simulating GoPro servers, and performing computer vision tasks such as object detection.

## Overview

This project provides tools for:
- Connecting to and processing GoPro camera streams
- Simulating a GoPro server using local video files
- Performing basic and advanced video analysis
- Object detection using pre-trained models

## Components

### GoPro Server Simulator
- **spoof_gopro_server_from_mp4_on_disk.py**: Creates a Flask server that simulates a GoPro camera by streaming a local MP4 file. The server implements GoPro-compatible API endpoints.

### Video Analysis Scripts
- **analyze_goPro.py**: Basic script that connects to a GoPro stream, applies simple image processing (grayscale conversion), and displays analysis metrics.
- **advanced_object_detect_goPro.py**: Advanced script that performs object detection on GoPro streams using a pre-trained MobileNet SSD model, focusing on detecting people and cars.
- **droid_cam_demo.py**: Similar to the advanced detection script but configured to work with an Android phone camera stream via the IP Webcam app.

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- Flask (for the server simulator)
- NumPy
- Requests

### Model Files (for object detection)
- `deploy.prototxt`
- `mobilenet_iter_73000.caffemodel`

## Usage

### Starting the GoPro Server Simulator
```bash
python spoof_gopro_server_from_mp4_on_disk.py
```
This will start a server on `http://localhost:8085` that simulates a GoPro camera using a local MP4 file.

### Running the Analysis Scripts
After starting the server simulator:

Basic analysis:
```bash
python analyze_goPro.py
```

Advanced object detection:
```bash
python advanced_object_detect_goPro.py
```

### Using with Android Phone Camera
To use with an Android phone camera:
1. Install the IP Webcam app on your Android device
2. Start the app and note the IP address and port
3. Update the `stream_url` in `droid_cam_demo.py` to match your phone's IP address
4. Run:
```bash
python droid_cam_demo.py
```

## Notes
- Press 'q' to exit any of the video processing scripts
- The object detection scripts are configured to detect and highlight people and cars
- The server simulator runs at 24fps by default
