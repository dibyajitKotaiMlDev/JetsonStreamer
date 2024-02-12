import cv2
from threading import Thread


class videocreate:
    def __init__(self, camera):
        self.cap = cv2.VideoCapture(camera)
        if not self.cap.isOpened():
            raise Exception("Error: Could not open camera.")
        self.frame = None
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while True:
            success, frame = self.cap.read()
            if not success:
                break
            else:
                # ret, jpeg = cv2.imencode('.jpg', frame)
                self.frame = frame

    def get_frame(self):
        return self.frame