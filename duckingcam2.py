from flask import Flask, render_template, Response
import cv2

app = Flask('hello')
camera0 = cv2.VideoCapture(0)  # CAP_DSHOW because of https://answers.opencv.org/question/234933/opencv-440modulesvideoiosrccap_msmfcpp-682-cvcapture_msmfinitstream-failed-to-set-mediatype-stream-0-640x480-30-mfvideoformat_rgb24unsupported-media/
camera2 = cv2.VideoCapture(2)
image0 = bytes()
image2 = bytes()


def gen_frames0():
    global image0
    while True:
        # print(time.time())
        success, image0 = camera0.read()
        if not success:
            print(" not success")
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + image0 + b'\r\n')
        else:
            ret, buffer = cv2.imencode('.jpg', image0)
            image0 = buffer.tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + image0 + b'\r\n')


def gen_frames2():
    global image2
    while True:
        # print(time.time())
        success, image2 = camera2.read()
        if not success:
            print(" not success")
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + image2 + b'\r\n')
        else:
            ret, buffer = cv2.imencode('.jpg', image2)
            image2 = buffer.tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + image2 + b'\r\n')


@app.route('/stream0')
def stream0():
    return Response(gen_frames0(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stream2')
def stream2():
    return Response(gen_frames2(), mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route('/')
# def index():
#     return """
# <body>
# <div class="container">
#     <div class="row">
#         <div class="col-lg-8  offset-lg-2">
#             <h3 class="mt-5">Live Streaming</h3>
#             <img src="/stream0" width="100%">
#         </div>
#     </div>
# </div>
# </body>
#     """



host = "0.0.0.0"
port = 8000
debug = False
options = None
app.run(host, port, debug, options)

