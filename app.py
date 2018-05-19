from flask import Flask, Response
from flask_restful import Resource, Api
from camera import Camera

application = Flask(__name__)
api = Api(application)

cam = Camera(application)


def gen_frames():
    '''
    Generator function, creates a comet of continous images
    '''
    try:
        while True:
            frame = cam.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except Exception as e:
        print(e)


class Stream(Resource):
    '''
    Streaming endpoint, starts a new thread to provide continous images
    '''
    def get(self):
        cam.stream_start()
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


class StreamStop(Resource):
    '''
    Stops streaming, free the camera resource
    '''
    def get(self):
        cam.stream_stop()
        return 200


class Capture(Resource):
    '''
    Capture an image / adds a new page to a document
    '''

    def get(self):
        cam.capture()
        return {
            'capture': 'ok',
            'streaming': cam.is_streaming(),
        }


class Hello(Resource):
    def get(self):
        return {
            'streaming': cam.is_streaming(),
        }


# actually bind rounting
api.add_resource(Stream, '/stream')
api.add_resource(StreamStop, '/stream/stop')
api.add_resource(Capture, '/capture')
api.add_resource(Hello, '/hello')


if __name__ == '__main__':
    application.run(host='0.0.0.0', threaded=False, debug=True)
