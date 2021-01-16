#!/usr/bin/env python
# -*- coding: utf-8 -*-  

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_humidity_v2 import BrickletHumidityV2
from tinkerforge.bricklet_barometer import BrickletBarometer
from tinkerforge.bricklet_ambient_light_v2 import BrickletAmbientLightV2

import logging as log
log.basicConfig(level=log.INFO)

from flask import send_from_directory
from flask import render_template
from flask import Flask       # Use Flask framework
application = Flask(__name__) # Function "application" is used by Apache/wsgi
app = application             # Use shortcut for routing

HOST = "localhost"
PORT = 4223
HUMIDITY_UID = "CXe" # Change to your UID
BAROMETER_UID = "vMM" # Change to your UID
AMBIENT_LIGHT_UID = "yJA" # Change to your UID

@app.route('/css/<path:path>')
def send_css(path):
    log.info('Path: ' + path)
    return send_from_directory('static/css', path)

@app.route('/js/<path:path>')
def send_js(path):
    log.info('Path: ' + path)
    return send_from_directory('static/js', path)

@app.route('/')
def index():
    ipcon = IPConnection() # Create IP connection
    humidity_bricklet = BrickletHumidityV2(HUMIDITY_UID, ipcon) # Create device object
    barometer_bricklet = BrickletBarometer(BAROMETER_UID, ipcon)
    ambient_light_bricklet = BrickletAmbientLightV2(AMBIENT_LIGHT_UID, ipcon)

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    temperature = humidity_bricklet.get_temperature()/100.0
    humidity = humidity_bricklet.get_humidity()/100.0
    air_pressure = barometer_bricklet.get_air_pressure()/1000.0
    illuminance = ambient_light_bricklet.get_illuminance()/100.0

    ipcon.disconnect()
    return render_template('index.html', temperature=temperature, humidity=humidity, illuminance=illuminance, air_pressure=air_pressure)
