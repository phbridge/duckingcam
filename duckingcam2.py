from flask import Flask, Response
import cv2
import wsgiserver
import time

camera = cv2.VideoCapture(2, cv2.CAP_GSTREAMER)
camera.release()

app = Flask('hello')


def _gen_frames(_camera):
    last_image = _camera.get(cv2.CAP_PROP_POS_MSEC)
    while True:
        if last_image == _camera.get(cv2.CAP_PROP_POS_MSEC):
            success, image = _camera.read()
        else:
            last_image = _camera.get(cv2.CAP_PROP_POS_MSEC)
            time.sleep(0.1)
            success, image = _camera.retrieve()
        if not success:
            print("not success read")
        else:
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
            ret, buffer = cv2.imencode('.jpg', image, encode_param)
            image = buffer.tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + image + b'\r\n')


@app.route('/stream2')
def stream2():
    print(camera.isOpened())
    if not camera.isOpened():
        camera.open(2)
    return Response(_gen_frames(_camera=camera), mimetype='multipart/x-mixed-replace; boundary=frame')


host = "0.0.0.0"
port = 8002
# app.run(host=host, port=port, debug=True)
http_server = wsgiserver.WSGIServer(host=host, port=port, wsgi_app=app)
http_server.start()

