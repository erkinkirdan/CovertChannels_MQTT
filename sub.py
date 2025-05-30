import paho.mqtt.client as mqtt
import time

TOPIC = "kgortlswe"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(TOPIC, qos=2)


storage_bitstring = ""
timing_bitstring = ""
last_message_time = 0
skip_first_timing = True
skip_first_storage = True


def bitstring_to_string(b):
    return "".join(chr(int(b[i : i + 8], 2)) for i in range(0, len(b), 8))


def on_message(client, userdata, msg):
    global storage_bitstring, timing_bitstring, last_message_time, skip_first_timing, skip_first_storage
    qos = msg.qos
    current_time = time.time()
    elapsed_time = current_time - last_message_time
    if elapsed_time >= 0.5:
        timing_bitstring += "1"
    else:
        timing_bitstring += "0"
    if timing_bitstring.endswith("11111111"):
        if not skip_first_timing:
            print("Timing secret: " + bitstring_to_string(timing_bitstring[:-8]))
        skip_first_timing = False
        timing_bitstring = ""
    last_message_time = current_time
    if qos == 2:
        if not skip_first_storage:
            print("Storage secret: " + bitstring_to_string(storage_bitstring))
        skip_first_storage = False
        storage_bitstring = ""
    else:
        storage_bitstring += str(qos)


if __name__ == "__main__":
    broker = input("Enter broker: ")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker)
    client.loop_forever()
