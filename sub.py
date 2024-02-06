import paho.mqtt.client as mqtt
import time

BROKER = "test.mosquitto.org"
TOPIC = "test/topic"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(TOPIC, qos=2)


storage_bitstring = ""
timing_bitstring = ""
storage_complete = False
timing_complete = False
last_message_time = None


def bitstring_to_string(b):
    return "".join(chr(int(b[i : i + 8], 2)) for i in range(0, len(b), 8))


def on_message(client, userdata, msg):
    global storage_bitstring, timing_bitstring, storage_complete, timing_complete, last_message_time
    qos = msg.qos
    current_time = time.time()
    if last_message_time is not None:
        elapsed_time = current_time - last_message_time
        if elapsed_time >= 0.75:
            timing_bitstring += "1"
        else:
            timing_bitstring += "0"
        if timing_bitstring.endswith("11111111"):
            if timing_complete:
                timing_secret = bitstring_to_string(timing_bitstring[:-8])
                print("Timing secret: " + timing_secret)
            else:
                timing_complete = True
            timing_bitstring = ""
    last_message_time = current_time
    if qos == 2:
        if storage_complete:
            storage_secret = bitstring_to_string(storage_bitstring)
            print("Storage secret: " + storage_secret)
            storage_bitstring = ""
        else:
            storage_complete = True
    elif storage_complete:
        bit = str(qos)
        storage_bitstring += bit


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER)
client.loop_forever()
