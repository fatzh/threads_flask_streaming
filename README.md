# threads_flask_streaming

Simple minimal FLask/Rest implementation of a REST server that can access a
resource (camera) and stream video in a threaded implementation.

The server stills accept concurrent requests (start uwsgi with multiple threads,
but just one process), and can stop the streaming thread.

The streaming thread is also automatically stop when inactive after X seconds.

This small demo generates random images to show a proof of concept.

The idea is to run this behind nginx/uwsgi in single process/single thread.

Anyway, that's just for info...

Install all requirements from `requirements.txt` file, run with
`FLASK_APP=app.py flask run` or `uwsgi --ini app.py`.
