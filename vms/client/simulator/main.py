import paho.mqtt.client as paho
from os import environ
import time
import json

from entity.sensor import Temperature, Pressure, Current, Humidity

broker = environ.get("SIM_HOST", "192.168.10.1")
port = int(environ.get("SIM_PORT", 1883))
name = environ.get("SIM_NAME", "sensor1")
period = int(environ.get("SIM_PERIOD", 5))
sim_type = environ.get("SIM_TYPE", "temperature")
topic_format = environ.get("SIM_TOPIC_FORMAT", "plain")

SENSORS = {"temperature": Temperature, "pressure": Pressure, "current": Current, "humidity": Humidity}

sensor = SENSORS[sim_type](name=name)


def on_connect(client, userdata, flags, rc):
    print(f"[{name}] Подключён к {broker}:{port}")


def on_publish(client, userdata, mid):
    print(f"[{name}] Опубликовано: {sensor.value}")


client = paho.Client(client_id=name)
client.on_connect = on_connect
client.on_publish = on_publish
client.connect(broker, port)
client.loop_start()

while True:
    sensor.generate_new_value()
    value = sensor.get_data()
    if topic_format == "json":
        topic = f"sensors/{sensor.type}"
        payload = json.dumps({"name": sensor.name, "value": value})
    else:
        topic = f"sensors/{sensor.type}/{sensor.name}"
        payload = str(value)
    client.publish(topic, payload)
    time.sleep(period)
