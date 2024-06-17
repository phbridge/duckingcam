from flask import Flask, Response
import cv2
import wsgiserver
import time

import paho.mqtt.client as mqtt
import paho
import json

app = Flask('hello')


MQTT_BROKER_URL = "mqtt.greenbridgetech.co.uk"
MQTT_USERNAME = "wifi_plugs"
MQTT_PASSWORD = "energymonitoring"


@app.route('/door_open')
def door_open():
    print("duckdoor open requested")
    # def on_connect(client, userdata, flags, rc):
    #     client.subscribe("zigbee2mqtt/bridge/request/device/options")

    # def on_message(client, userdata, msg):
    #     print(msg)

    # def _mqtt_time():
    #     """Return current time string for mqtt messages."""
    #     return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    duckdoor = "zigbee2mqtt/Curtains/DuckDoor/set"
    # mqttc = mqtt.Client()
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    mqttc.connect(MQTT_BROKER_URL)
    duckdoor_ = {
        "state": "CLOSE"
    }
    # mqttc.on_connect = on_connect
    # mqttc.on_message = on_message
    mqttc.publish(topic=duckdoor, payload=json.dumps(duckdoor_))
    print("duckdoor open sent")
    mqttc.disconnect()
    return Response("OPENING", mimetype='text/plain')


@app.route('/door_close')
def door_close():
    print("duckdoor close requested")
    # def on_connect(client, userdata, flags, rc):
    #     client.subscribe("zigbee2mqtt/bridge/request/device/options")

    # def on_message(client, userdata, msg):
    #     print(msg)

    # def _mqtt_time():
    #     """Return current time string for mqtt messages."""
    #     return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    duckdoor = "zigbee2mqtt/Curtains/DuckDoor/set"
    # mqttc = mqtt.Client()
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    mqttc.connect(MQTT_BROKER_URL)
    duckdoor_ = {
        "state": "OPEN"
    }
    # mqttc.on_connect = on_connect
    # mqttc.on_message = on_message
    mqttc.publish(topic=duckdoor, payload=json.dumps(duckdoor_))
    print("duckdoor close sent")
    mqttc.disconnect()
    return Response("CLOSING", mimetype='text/plain')


host = "0.0.0.0"
port = 8888
# app.run(host=host, port=port)
# http_server = wsgiserver.WSGIServer(host=host, port=port, wsgi_app=app, certfile=, keyfile=)
http_server = wsgiserver.WSGIServer(host=host, port=port, wsgi_app=app)
http_server.start()

