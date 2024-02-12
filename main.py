import cv2
import os
from flask import Flask, Response, render_template, request
import datetime
from camera import *
app = Flask(__name__)

# Replace with your RTSP URL and credentials if needed
RTSP_URL = "rtsp://admin:pass@123@192.168.1.240:554/cam/realmonitor?channel=2&subtype=0"
RTSP_URL2 = "rtsp://admin:pass@123@192.168.1.240:554/cam/realmonitor?channel=1&subtype=0"

# Recording settings
RECORD_DIRECTORY = "recordings"  # Update with your desired directory
record_flag = False  # Flag to control recording
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Video codec for AVI file
avi_filename = None  # Variable to store AVI file name
video_writer = None

## for secoend cam
# Video writer object
avi_filename2 = None  # Variable to store AVI file name
video_writer2 = None
video_captures = videocreate(RTSP_URL)
video_captures2cam = videocreate(RTSP_URL2)
def gen_frames():
    global video_writer
    # cap = cv2.VideoCapture(RTSP_URL)

    while True:
        frame = video_captures.get_frame()

        if record_flag:
            if video_writer is None:
                timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
                avi_filename = os.path.join(RECORD_DIRECTORY, "cam1"+timestamp + ".avi")
                video_writer = cv2.VideoWriter(avi_filename, fourcc, 20.0, (frame.shape[1], frame.shape[0]))

            video_writer.write(frame)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def gen_frames2cam():
    global video_writer2
    # cap = cv2.VideoCapture(RTSP_URL)

    while True:
        frame = video_captures2cam.get_frame()

        if record_flag:
            if video_writer2 is None:
                timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
                avi_filename2 = os.path.join(RECORD_DIRECTORY, "cam2"+timestamp + ".avi")
                video_writer2 = cv2.VideoWriter(avi_filename2, fourcc, 20.0, (frame.shape[1], frame.shape[0]))

            video_writer2.write(frame)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    global record_flag
    record_button_text = "Start Recording" if not record_flag else "Stop Recording"
    return render_template('index.html', record_button_text=record_button_text)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_feed2cam')
def video_feed2cam():
    return Response(gen_frames2cam(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/toggle_record')
def toggle_record():
    global record_flag, video_writer, avi_filename,video_writer2,avi_filename2
    print("check the record flag stat : ",record_flag)
    # record_flag = not record_flag
    ## make the record flag True else false
    if record_flag:
        record_flag = False
        video_writer.release()
        video_writer = None
        avi_filename = None
        video_writer2.release()
        video_writer2 = None
        avi_filename2 = None
        return "Start Recording"
    else:
        record_flag = True
        return "Stop Recording"


if __name__ == '__main__':
    os.makedirs(RECORD_DIRECTORY, exist_ok=True)  # Create recording directory if not exists
    app.run(host='0.0.0.0', debug=True)  # Adjust host and debug as needed
