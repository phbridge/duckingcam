from flask import Flask, Response
import cv2
import threading

app = Flask(__name__)
lock = threading.Lock()


@app.route('/stream0', methods=['GET'])
def stream0():
    return Response(generate(cam_index=0), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/stream1', methods=['GET'])
def stream1():
    return Response(generate(cam_index=1), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/stream2', methods=['GET'])
def stream2():
    return Response(generate(cam_index=1), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/stream3', methods=['GET'])
def stream3():
    return Response(generate(cam_index=1), mimetype="multipart/x-mixed-replace; boundary=frame")


def generate(cam_index=0):
    global lock
    vc = cv2.VideoCapture(cam_index)
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False
    while rval:
        with lock:
            rval, frame = vc.read()
            if frame is None:
                continue
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            if not flag:
                continue
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
    vc.release()


if __name__ == '__main__':
    host = "127.0.0.1"
    port = 8000
    debug = False
    options = None
    app.run(host, port, debug, options)