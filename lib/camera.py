import cv2, queue, threading
# cap = cv2.VideoCapture('libcamerasrc ! video/x-raw,framerate=100/1,width=640,height=480 ! videoscale ! videoconvert ! appsink drop=true sync=false', cv2.CAP_GSTREAMER)

class VideoCapture:
    def __init__(self, name):
        self.cap = cv2.VideoCapture(name, cv2.CAP_GSTREAMER)
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()