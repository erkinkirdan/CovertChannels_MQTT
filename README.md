# Covert Channel Attacks on MQTT

This repository hosts a demonstration of covert channel attacks on MQTT.

The demonstration involves two components:

- A publisher script that encodes secrets into timing delays and QoS levels.
- A subscriber script that decodes the timing delays and QoS levels back into the secrets.

## Installation

1. Clone the repository: `git clone https://github.com/erkinkirdan/CovertChannelAttacks_MQTT.git`
2. Navigate into the cloned repository: `cd CovertChannelAttacks_MQTT`
3. Create a virtual environment: `python3 -m venv env`
4. Activate the virtual environment: `source env/bin/activate`
5. Install the necessary Python modules using pip: `pip install paho-mqtt`

## Running

To run the publisher:

```bash
python pub.py
```

To run the subscriber:

```bash
python sub.py
```
