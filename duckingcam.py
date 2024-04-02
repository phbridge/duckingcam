from flask import Flask, Response
import cv2
import threading

app = Flask(__name__)
lock0 = threading.Lock()
lock2 = threading.Lock()

encodedImage0 = bytearray()
encodedImage2 = bytearray()


@app.route('/stream0', methods=['GET'])
def stream0():
    return Response(generate(cam_index=0), mimetype="multipart/x-mixed-replace; boundary=frame")


# @app.route('/stream1', methods=['GET'])
# def stream1():
#     return Response(generate(cam_index=1), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/stream2', methods=['GET'])
def stream2():
    return Response(generate2(cam_index=2), mimetype="multipart/x-mixed-replace; boundary=frame")


# @app.route('/stream3', methods=['GET'])
# def stream3():
#     return Response(generate(cam_index=3), mimetype="multipart/x-mixed-replace; boundary=frame")


def generate(cam_index=0):
    global lock0
    print(lock0)
    vc = cv2.VideoCapture(0)
    # vc = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
    # vc = cv2.VideoCapture(cam_index, cv2.CAP_V4L)
    # vc = cv2.VideoCapture(cam_index, cv2.CAP_V4L2)
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False
        print(" is false")
    while rval:
        # with lock:
        rval, frame = vc.read()
        if frame is None:
            continue
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        if not flag:
            continue
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
    vc.release()


def generate2(cam_index=2):
    global lock2
    global encodedImage2
    print(lock2)
    if not lock2.locked():
        vc = cv2.VideoCapture(2)
    # vc = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
    # vc = cv2.VideoCapture(cam_index, cv2.CAP_V4L)
    # vc = cv2.VideoCapture(cam_index, cv2.CAP_V4L2)
        if vc.isOpened():
            rval, frame = vc.read()
        else:
            rval = False
            print(" is false")
        while rval:
            # with lock:
            rval, frame = vc.read()
            if frame is None:
                continue
            (flag, encodedImage2) = cv2.imencode(".jpg", frame)
            if not flag:
                continue
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage2) + b'\r\n')
        vc.release()
    else:
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage2) + b'\r\n')


if __name__ == '__main__':
    host = "0.0.0.0"
    port = 8000
    debug = False
    options = None
    app.run(host, port, debug, options)

