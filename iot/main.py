import machine
import network
import time
import json
import onewire
import ds18x20
from umqttsimple import MQTTClient

PIN = 4
SLEEP = 5
IDENTITY_FILE = "identity.json"
SETTINGS_FILE = "settings.json"

identity = None
topic = None


def getFileContent(fileName):
    file = open(fileName, "r")
    return file.read()


def getValue(content, key):
    if isinstance(content, dict):
        # Passed argument is already a JSON dictionary
        return content[key]
    else:
        # Passed argument seems to be a String
        return json.loads(content)[key]


def connect():
    # Load WiFi settings
    settingsFileContent = getFileContent(SETTINGS_FILE)
    wifiSettings = getValue(settingsFileContent, "wifi")
    wifiSsid = getValue(wifiSettings, "ssid")
    wifiPassword = getValue(wifiSettings, "password")

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
    mqttSettings = getValue(settingsFileContent, "mqtt")
    mqttUsername = getValue(mqttSettings, "username")
    mqttPassword = getValue(mqttSettings, "password")
    mqttBrokerAddress = getValue(mqttSettings, "brokerAddress")

    # Load identity settings
    identityFileContent = getFileContent(IDENTITY_FILE)
    identity = getValue(identityFileContent, "identity")

    # Connect to broker
    client = MQTTClient(identity, mqttBrokerAddress, user=mqttUsername, password=mqttPassword)
    client.connect()

    print("Set up MQTT client", identity)
    return client


connect()

client = getMqttClient()

pin = machine.Pin(PIN)
sensor = ds18x20.DS18X20(onewire.OneWire(pin))
roms = sensor.scan()

identityFileContent = getFileContent(IDENTITY_FILE)
identity = getValue(identityFileContent, "identity")
topicFormat = getValue(identityFileContent, "topicFormat")
topic = topicFormat.replace("{id}", identity)

while True:
    sensor.convert_temp()
    for rom in roms:
        temperature = sensor.read_temp(rom)
        print("Measured temperature", temperature)
        client.publish(topic, str(temperature))
    time.sleep(SLEEP)
