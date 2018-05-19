# threads_flask_streaming

Simple minimal FLask/Rest implementation of a REST server that can access a resource (camera) and stream video in a threaded implementation.

The server stills accept concurrent requests (start flask in threaded mode), and can stop the streaming thread.

The streaming thread is also automatically stop w hen inactive.

This small demo generates random images to show a proof of concept.

The idea is to run this behind nginx/uwsgi in single process/single thread. Activate `enable-threads` in uwsgi configuration to allow only for the streaming thread.

Otherwise we have some issues when multiple uwsgi/nginx processes/threads are trying to access the same camera (only one physical camera).

Anyway, that's just for info...

Install all requirements from `requirements.txt` file, run with `FLASK_APP=app.py flask run`.
