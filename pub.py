import paho.mqtt.client as mqtt
import time

TOPIC = "kgortlswe"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def sleep(timing_bitstring, sleep_index):
    if timing_bitstring[sleep_index] == "1":
        time.sleep(1)
    else:
        time.sleep(0.1)
    return (sleep_index + 1) % len(timing_bitstring)


def publish(storage_bitstring, timing_bitstring):
    sleep_index = 0
    while True:
        for bit in storage_bitstring:
            qos = int(bit)
            client.publish(TOPIC, qos=qos)
            sleep_index = sleep(timing_bitstring, sleep_index)
        client.publish(TOPIC, qos=2)
        sleep_index = sleep(timing_bitstring, sleep_index)


def string_to_bitstring(s):
    return "".join(format(ord(c), "08b") for c in s)


if __name__ == "__main__":
    broker = input("Enter broker: ")
    storage_secret = input("Enter storage secret: ")
    timing_secret = input("Enter timing secret: ")
    storage_bitstring = string_to_bitstring(storage_secret)
    timing_bitstring = string_to_bitstring(timing_secret)
    timing_bitstring = timing_bitstring + "11111111"
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(broker)
    client.loop_start()
    publish(storage_bitstring, timing_bitstring)
