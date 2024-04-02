from flask import Flask, render_template, Response
import cv2

camera0 = cv2.VideoCapture(0)
camera0.release()
camera2 = cv2.VideoCapture(2)
camera2.release()

app = Flask('hello')


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
        success, image = camera.retrieve()
        if not success:
            print("not success")
        else:
            ret, buffer = cv2.imencode('.jpg', image)
            image = buffer.tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + image + b'\r\n')


def gen_frames(camera):
    while True:
        success, image = camera.read()
        if not success:
            print("not success")
        else:
            ret, buffer = cv2.imencode('.jpg', image)
            image = buffer.tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + image + b'\r\n')


@app.route('/stream0')
def stream0():
    print(camera0.isOpened())
    if camera0.isOpened():
        return Response(read_frames(camera=camera0), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        camera0.open(0)
        return Response(gen_frames(camera=camera0), mimetype='multipart/x-mixed-replace; boundary=frame')
    return "ERROR"


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


# cam0thread = threading.Thread(target=lambda: gen_frames0())
# cam0thread.start()
# cam2thread = threading.Thread(target=lambda: gen_frames2())
# cam2thread.start()


host = "0.0.0.0"
port = 8000
debug = False
options = None
threaded = True
app.run(host, port, debug, options, threaded)

