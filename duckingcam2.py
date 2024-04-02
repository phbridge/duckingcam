from flask import Flask, render_template, Response
import cv2, time

app = Flask('hello')
camera0 = cv2.VideoCapture(0)  # CAP_DSHOW because of https://answers.opencv.org/question/234933/opencv-440modulesvideoiosrccap_msmfcpp-682-cvcapture_msmfinitstream-failed-to-set-mediatype-stream-0-640x480-30-mfvideoformat_rgb24unsupported-media/
camera2 = cv2.VideoCapture(2)
image0 = None
image2 = None


def gen_frames():
    global image0, image2
    while True:
        # print(time.time())
        success, image0 = camera0.read()
        success, image2 = camera2.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', image0)
            ret, buffer = cv2.imencode('.jpg', image2)
            image0 = buffer.tobytes()
            image2 = buffer.tobytes()
            # yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + image0 + b'\r\n')
            yield


@app.route('/stream0')
def stream0():
    gen_frames()
    return Response(b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + image0 + b'\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stream2')
def stream2():
    gen_frames()
    return Response(b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + image2 + b'\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')


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

