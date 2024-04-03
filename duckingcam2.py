from flask import Flask, render_template, Response
import cv2
import wsgiserver
import time
import threading

camera0 = cv2.VideoCapture(0, cv2.CAP_GSTREAMER)
camera0.release()
camera2 = cv2.VideoCapture(2, cv2.CAP_GSTREAMER)
camera2.release()

cv2.VideoWriter()
app = Flask('hello')

backup = [bytes(), bytes(), bytes()]

# def gen_frames0():
#     global image0
#     while True:
#         # print(time.time())
#         success, _image0 = camera0.read()
#         if not success:
#             print("not success 0")
#             yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + image0 + b'\r\n')
#         else:
#             ret, buffer = cv2.imencode('.jpg', _image0)
#             image0 = buffer.tobytes()
#             yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + image0 + b'\r\n')


def read_frames(camera):
    while True:
        time.sleep(0.1)
        success, image = camera.retrieve()
        if not success:
            print("not success")
        else:
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
            # ret, buffer = cv2.imencode('.jpg', image)
            ret, buffer = cv2.imencode('.jpg', image, encode_param)
            image = buffer.tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + image + b'\r\n')

        # ret, buffer = cv2.imencode('.jpg', backup[backup_int])
        # image = buffer.tobytes()
        # # yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
        # yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + backup[backup_int] + b'\r\n')


def gen_frames_only():
    while True:
        # success, image = camera0.grab()
        # success, image = camera2.grab()
        camera0.grab()
        camera2.grab()
        time.sleep(0.03)


def gen_frames(camera):
    while True:
        success, image = camera.read()
        if not success:
            print("not success")
        else:
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 95]
            # ret, buffer = cv2.imencode('.jpg', image)
            ret, buffer = cv2.imencode('.jpg', image, encode_param)
            # image = buffer.tobytes()
            image = buffer.tobytes()
            # yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + image + b'\r\n')


@app.route('/stream0')
def stream0():
    # print(camera0.isOpened())
    # if camera0.isOpened():
    #     return Response(read_frames(camera=camera0), mimetype='multipart/x-mixed-replace; boundary=frame')
    # else:
    #     camera0.open(0)
    #     return Response(gen_frames(camera=camera0), mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(read_frames(camera=camera0), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stream2')
def stream2():
    global image2
    print(camera2.isOpened())
    if camera2.isOpened():
        return Response(read_frames(camera=camera2), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        camera2.open(2)
        return Response(gen_frames(camera=camera2), mimetype='multipart/x-mixed-replace; boundary=frame')
    return "ERROR"


camgrab = threading.Thread(target=lambda: gen_frames_only())
camgrab.start()


host = "0.0.0.0"
port = 8000
debug = False
options = None
threaded = True
processes = 1
# app.run(host=host, port=port, debug=debug)
http_server = wsgiserver.WSGIServer(host=host, port=port, wsgi_app=app)
http_server.start()

