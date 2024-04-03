from flask import Flask, Response
import cv2
import wsgiserver
import time
import threading

camera0 = cv2.VideoCapture(0, cv2.CAP_GSTREAMER)
camera0.release()
camera2 = cv2.VideoCapture(2, cv2.CAP_GSTREAMER)
camera2.release()

app = Flask('hello')


def read_frames(camera):
    last_image = camera.get(cv2.CAP_PROP_POS_MSEC)
    while True:
        if last_image == camera.get(cv2.CAP_PROP_POS_MSEC):
            success, image = camera.read()
        else:
            last_image = camera.get(cv2.CAP_PROP_POS_MSEC)
            time.sleep(0.1)
            success, image = camera.retrieve()
        if not success:
            print("not success read")
        else:
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
            ret, buffer = cv2.imencode('.jpg', image, encode_param)
            image = buffer.tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + image + b'\r\n')


def gen_frames(camera):
    last_image = camera.get(cv2.CAP_PROP_POS_MSEC)
    while True:
        if last_image == camera.get(cv2.CAP_PROP_POS_MSEC):
            success, image = camera.read()
        else:
            last_image = camera.get(cv2.CAP_PROP_POS_MSEC)
            time.sleep(0.1)
            success, image = camera.retrieve()
        if not success:
            print("not success read")
        else:
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
            ret, buffer = cv2.imencode('.jpg', image, encode_param)
            image = buffer.tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + image + b'\r\n')


def gen_always():
    global camera0
    global camera2
    while True:
        camera0.open(0)
        camera2.open(2)
        camera0.grab()
        camera2.grab()
        time.sleep(0.05)


@app.route('/stream0')
def stream0():
    print(camera0.isOpened())
    if camera0.isOpened():
        return Response(read_frames(camera=camera0), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        camera0.open(0)
        return Response(gen_frames(camera=camera0), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stream2')
def stream2():
    print(camera2.isOpened())
    if camera2.isOpened():
        return Response(read_frames(camera=camera2), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        camera2.open(2)
        return Response(gen_frames(camera=camera2), mimetype='multipart/x-mixed-replace; boundary=frame')


gen_always_thread = threading.Thread(target=lambda: gen_always())
gen_always_thread.start()


host = "0.0.0.0"
port = 8000
app.run(host=host, port=port, debug=True)


# http_server = wsgiserver.WSGIServer(host=host, port=port, wsgi_app=app)
# http_server.start()


