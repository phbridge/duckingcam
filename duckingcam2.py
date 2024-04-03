from flask import Flask, Response
import cv2
import wsgiserver
import time

# camera0 = cv2.VideoCapture(0, cv2.CAP_GSTREAMER)
# camera0.release()
camera = cv2.VideoCapture(2, cv2.CAP_GSTREAMER)
camera.release()

app = Flask('hello')

#
# def read_frames(camera):
#     last_image = camera.get(cv2.CAP_PROP_POS_MSEC)
#     while True:
#         if last_image == camera.get(cv2.CAP_PROP_POS_MSEC):
#             success, image = camera.read()
#         else:
#             last_image = camera.get(cv2.CAP_PROP_POS_MSEC)
#             time.sleep(0.1)
#             success, image = camera.retrieve()
#         if not success:
#             print("not success read")
#         else:
#             encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
#             ret, buffer = cv2.imencode('.jpg', image, encode_param)
#             image = buffer.tobytes()
#             yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + image + b'\r\n')


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



# @app.route('/stream0')
# def stream0():
#     print(camera0.isOpened())
#     if camera0.isOpened():
#         return Response(read_frames(camera=camera0), mimetype='multipart/x-mixed-replace; boundary=frame')
#     else:
#         camera0.open(0)
#         return Response(gen_frames(camera=camera0), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stream2')
def stream2():
    print(camera.isOpened())
    if not camera.isOpened():
        camera.open(2)
    return Response(_gen_frames(_camera=camera), mimetype='multipart/x-mixed-replace; boundary=frame')


host = "0.0.0.0"
port = 8002
app.run(host=host, port=port, debug=True)


# http_server = wsgiserver.WSGIServer(host=host, port=port, wsgi_app=app)
# http_server.start()


