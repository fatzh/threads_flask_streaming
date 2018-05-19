from PIL import Image
import io
import time
from random import randint
import threading

STREAM_TIMEOUT = 2


class Camera():

    application = None
    streaming = False  # class variable, used to check the current status

    frame = None  # current frame from streaming
    last_frame_request = None  # timestamp last requested frame from streaming, to free resources in case of inactivity

    thread = None  # that's the streaming thread

    def __init__(self, app):
        self.application = app

    def stream_start(self):
        Camera.last_frame_request = time.time()
        Camera.streaming = True
        if Camera.thread is None:
            Camera.thread = threading.Thread(target=Camera._stream)
            print('STARTING STREAMING THREAD')
            Camera.thread.start()
        while Camera.frame is None:
            time.sleep(0.05)
        return True

    def stream_stop(self):
        if Camera.streaming or Camera.thread:
            Camera.streaming = False
            try:
                Camera.thread.join()
            except AttributeError:
                pass
            Camera.thread = None
        return 200

    @classmethod
    def _stream(cls):
        while(cls.streaming and time.time() - cls.last_frame_request < STREAM_TIMEOUT):
            time.sleep(0.5)
            g = randint(0, 255)
            r = randint(0, 255)
            b = randint(0, 255)
            img = Image.new('RGB', (800, 800), (r, g, b))
            out = io.BytesIO()
            img.save(out, format='JPEG')
            cls.frame = out.getvalue()

        # we arrive here if streaming is set to Flase (by stream_stop for
        # example) or if no frame has been requested in the last X seconds
        print('STOPPING STREAMING THREAD')
        cls.streaming = False
        cls.thread = None

    def get_frame(self):
        Camera.last_frame_request = time.time()
        return self.frame

    def capture(self):
        self.stream_stop()
        return True

    def is_streaming(self):
        return Camera.streaming
