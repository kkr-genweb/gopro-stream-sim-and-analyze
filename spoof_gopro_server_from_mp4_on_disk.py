from flask import Flask, Response, jsonify, request
import cv2
import time

app = Flask(__name__)

# Load a sample video
# Ensure the video file is in the same directory as your script.
video_source = "person-bicycle-car-detection.mp4"
cap = cv2.VideoCapture(video_source)

# Simulated API state
camera_state = {
    "streaming": False,
    "mode": "video",
    "battery": 85
}

def generate_frames():
    """Reads frames from the video, looping it when it ends."""
    while camera_state["streaming"]:
        success, frame = cap.read()
        if not success:
            # If the video has ended, reset the capture to the first frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue  # Continue to the next iteration to read the new frame

        # Encode the frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        if buffer is None:
            continue
        
        frame_bytes = buffer.tobytes()

        # Yield the frame in the multipart format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        # Control the frame rate
        time.sleep(1/24)  # Simulate 24fps

@app.route('/gp/gpControl/execute', methods=['GET'])
def control():
    p1 = request.args.get('p1')
    a1 = request.args.get('a1')
    c1 = request.args.get('c1')

    if p1 == "gpStream" and a1 == "proto_v2" and c1 == "restart":
        if not camera_state["streaming"]:
            # Reset video to the beginning every time stream starts
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            camera_state["streaming"] = True
            print("Streaming started.")
        return jsonify({"status": "streaming started"})
    return jsonify({"status": "unknown command"})

@app.route('/live/preview')
def video_feed():
    if not camera_state["streaming"]:
        return "Stream not started. Please start the stream via the /gp/gpControl/execute endpoint.", 400
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/gp/gpControl/status')
def status():
    return jsonify(camera_state)

# A more conventional endpoint to stop the stream
@app.route('/gp/gpControl/stream/stop', methods=['GET', 'POST'])
def stop_stream():
    camera_state["streaming"] = False
    print("Streaming stopped.")
    return jsonify({"status": "streaming stopped"})

if __name__ == '__main__':
    # Using threaded=True to handle multiple requests
    app.run(host='0.0.0.0', port=8085, debug=True, threaded=True)