import machine
import network
import time
import json
import onewire
import ds18x20
from umqttsimple import MQTTClient

PIN = 4
SLEEP = 5

# Invalid temperature measurement (because of poor cables or whatever)
DISCARD_SENSOR_VALUE = 85

TOPIC_IDENTITY_PLACEHOLDER = "{id}"
IDENTITY_FILE = "identity.json"
SETTINGS_FILE = "settings.json"


def getFileContent(fileName):
    file = open(fileName, "r")
    return file.read()


def getValueFromJson(jsonContent, key):
    if isinstance(jsonContent, dict):
        # Passed argument is already a JSON dictionary
        return jsonContent[key]
    else:
        # Passed argument seems to be a String
        return json.loads(jsonContent)[key]


def connect():
    # Load WiFi settings
    settingsFileContent = getFileContent(SETTINGS_FILE)
    wifiSettings = getValueFromJson(settingsFileContent, "wifi")
    wifiSsid = getValueFromJson(wifiSettings, "ssid")
    wifiPassword = getValueFromJson(wifiSettings, "password")

    # Connect to network
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(wifiSsid, wifiPassword)

    while station.isconnected() == False:
        pass

    print("Connected to", wifiSsid)


def getMqttClient():
    # Load MQTT settings
    settingsFileContent = getFileContent(SETTINGS_FILE)
    mqttSettings = getValueFromJson(settingsFileContent, "mqtt")
    mqttUsername = getValueFromJson(mqttSettings, "username")
    mqttPassword = getValueFromJson(mqttSettings, "password")
    mqttBrokerAddress = getValueFromJson(mqttSettings, "brokerAddress")

    # Load identity settings
    identityFileContent = getFileContent(IDENTITY_FILE)
    identity = getValueFromJson(identityFileContent, "identity")

    # Connect to broker
    client = MQTTClient(identity, mqttBrokerAddress, user=mqttUsername, password=mqttPassword)
    client.connect()

    print("Set up MQTT client for", identity)
    return client


connect()

client = getMqttClient()

pin = machine.Pin(PIN)
sensor = ds18x20.DS18X20(onewire.OneWire(pin))
roms = sensor.scan()

identityFileContent = getFileContent(IDENTITY_FILE)
identity = getValueFromJson(identityFileContent, "identity")
topicFormat = getValueFromJson(identityFileContent, "topicFormat")
topic = topicFormat.replace(TOPIC_IDENTITY_PLACEHOLDER, identity)

while True:
    sensor.convert_temp()

    for rom in roms:
        temperature = sensor.read_temp(rom)

        if temperature != DISCARD_SENSOR_VALUE:
            print("Measured temperature", temperature)
            client.publish(topic, str(temperature))

            time.sleep(SLEEP)
