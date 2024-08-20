import time

from flask import Flask, Response
# import cv2
import wsgiserver
# import time

import paho.mqtt.client as mqtt
# import paho
import json
import signal
from suntimes import SunTimes
from datetime import datetime, date, timedelta
import threading
import logging.handlers                 # Needed for logging
import inspect
import sys
import traceback


ABSOLUTE_PATH = "/home/phbridge/duckingcam"
LOGFILE = ABSOLUTE_PATH + "/logs/ducking.log"

app = Flask('ducking_door')

MQTT_BROKER_URL = "mqtt.greenbridgetech.co.uk"


THREAD_TO_BREAK = threading.Event()

SUN = SunTimes(longitude=-2.710632, latitude=53.743913, altitude=0)


@app.route('/door_open')
def door_open():
    function_logger = logger.getChild("%s.%s.%s" % (inspect.stack()[2][3], inspect.stack()[1][3], inspect.stack()[0][3]))
    function_logger.info("duckdoor open requested")
    duckdoor = "zigbee2mqtt/Curtains/DuckDoor/set"
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    mqttc.connect(MQTT_BROKER_URL)
    duckdoor_ = {
        "state": "CLOSE"
    }
    sent = 0
    while sent < 15:
        mqttc.publish(topic=duckdoor, payload=json.dumps(duckdoor_))
        function_logger.info("duck door open sent")
        sent += 1
        time.sleep(120)
    mqttc.disconnect()
    return Response("OPENING", mimetype='text/plain')


@app.route('/door_close')
def door_close():
    function_logger = logger.getChild("%s.%s.%s" % (inspect.stack()[2][3], inspect.stack()[1][3], inspect.stack()[0][3]))
    function_logger.info("duckdoor close requested")
    duckdoor = "zigbee2mqtt/Curtains/DuckDoor/set"
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    mqttc.connect(MQTT_BROKER_URL)
    duckdoor_ = {
        "state": "OPEN"
    }
    sent = 0
    while sent < 15:
        mqttc.publish(topic=duckdoor, payload=json.dumps(duckdoor_))
        function_logger.info("duck door close sent")
        sent += 1
        time.sleep(120)
    mqttc.disconnect()
    return Response("CLOSING", mimetype='text/plain')




# datetime.date.today() + datetime.timedelta(days=1)
# datetime.date.today() + datetime.timedelta(days=1)
#
datetime.today()
# day = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
# print(SUN.setwhere(date=day, elsewhere="Europe/London"))
# print(SUN.risewhere(date=day, elsewhere="Europe/London"))


def master_timer_sunrise():
    function_logger = logger.getChild("%s.%s.%s" % (inspect.stack()[2][3], inspect.stack()[1][3], inspect.stack()[0][3]))
    first_run = True
    while not THREAD_TO_BREAK.is_set():
        if not first_run:
            if THREAD_TO_BREAK.is_set():
                return
            try:
                door_open()
            except Exception as e:
                function_logger.error("something went bad with auto_webscrape")
                function_logger.error("Unexpected error:" + str(sys.exc_info()[0]))
                function_logger.error("Unexpected error:" + str(e))
                function_logger.error("TRACEBACK=" + str(traceback.format_exc()))
        first_run = False
        t = datetime.today()
        future = SUN.risewhere(date=datetime.today(), elsewhere="Europe/London")
        function_logger.info("sunrise sleeping for %s" % (future - t).seconds)
        if (future - t).seconds < 1:
            future += timedelta(days=1)
        function_logger.info("sunrise sleeping for %s" % (future - t).seconds)
        THREAD_TO_BREAK.wait((future - t).seconds)


def master_timer_sunset():
    function_logger = logger.getChild("%s.%s.%s" % (inspect.stack()[2][3], inspect.stack()[1][3], inspect.stack()[0][3]))
    first_run = True
    while not THREAD_TO_BREAK.is_set():
        if not first_run:
            if THREAD_TO_BREAK.is_set():
                return
            try:
                door_close()
            except Exception as e:
                function_logger.error("something went bad with auto_webscrape")
                function_logger.error("Unexpected error:" + str(sys.exc_info()[0]))
                function_logger.error("Unexpected error:" + str(e))
                function_logger.error("TRACEBACK=" + str(traceback.format_exc()))
        first_run = False
        t = datetime.today()
        future = SUN.setwhere(date=datetime.today(), elsewhere="Europe/London")
        function_logger.info("sunset sleeping for %s" % (future - t).seconds)
        if (future - t).seconds < 1:
            future += timedelta(days=1)
        function_logger.info("sunset sleeping for %s" % (future - t).seconds)
        THREAD_TO_BREAK.wait((future - t).seconds)


def graceful_killer(signal_number, frame):
    function_logger = logger.getChild("%s.%s.%s" % (inspect.stack()[2][3], inspect.stack()[1][3], inspect.stack()[0][3]))
    function_logger.critical("Got Kill signal")
    function_logger.critical('Received:' + str(signal_number))
    THREAD_TO_BREAK.set()
    function_logger.critical("set threads to break")
    master_timer_sunrise_thread.join()
    master_timer_sunset_thread.join()
    quit()


if __name__ == "__main__":
    # Create Logger
    logger = logging.getLogger("%s.__main__" % "ccl_web_scraper")
    # handler = logging.handlers.RotatingFileHandler(LOGFILE, maxBytes=LOGFILE_MAX_SIZE, backupCount=LOGFILE_COUNT)
    handler = logging.handlers.TimedRotatingFileHandler(LOGFILE, backupCount=90, when='D')
    logger_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(process)d:%(name)s - %(message)s')
    # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(logger_formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.info("---------------------- STARTING ----------------------")
    logger.info("ccl web scraper script started")

    # Catch SIGTERM etc
    signal.signal(signal.SIGHUP, graceful_killer)
    signal.signal(signal.SIGTERM, graceful_killer)

    # start the sunrise/sunset auto actions
    master_timer_sunrise_thread = threading.Thread(target=lambda: master_timer_sunrise())
    master_timer_sunrise_thread.start()
    master_timer_sunset_thread = threading.Thread(target=lambda: master_timer_sunset())
    master_timer_sunset_thread.start()




host = "0.0.0.0"
port = 8888
# app.run(host=host, port=port)
# http_server = wsgiserver.WSGIServer(host=host, port=port, wsgi_app=app, certfile=, keyfile=)
http_server = wsgiserver.WSGIServer(host=host, port=port, wsgi_app=app)
http_server.start()

