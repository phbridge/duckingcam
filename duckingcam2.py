from flask import Flask, render_template, Response
import cv2
import threading


app = Flask('hello')


image0 = bytes()
image2 = bytes()

def gen_frames0():
    camera0 = cv2.VideoCapture(0)
    global image0
    while True:
        # print(time.time())
        success, _image0 = camera0.read()
        if not success:
            print(" not success")
        else:
            ret, buffer = cv2.imencode('.jpg', _image0)
            image0 = buffer.tobytes()



def gen_frames2():
    camera2 = cv2.VideoCapture(2)
    global image2
    while True:
        # print(time.time())
        success, _image2 = camera2.read()
        if not success:
            print(" not success")
        else:
            ret, buffer = cv2.imencode('.jpg', _image2)
            image2 = buffer.tobytes()

            # yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + image2 + b'\r\n')


@app.route('/stream0')
def stream0():
    return Response(b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + image0 + b'\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stream2')
def stream2():
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

cam0thread = threading.Thread(target=lambda: gen_frames0())
cam0thread.start()
cam2thread = threading.Thread(target=lambda: gen_frames2())
cam2thread.start()


host = "0.0.0.0"
port = 8000
debug = False
options = None
app.run(host, port, debug, options)

