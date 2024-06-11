import paho.mqtt.client as mqtt
import json
import random
import time

# ThingsBoard parameters
THINGSBOARD_HOST = 'demo.thingsboard.io'
ACCESS_TOKEN = 'NsSXgwy3UIiQIDm5Wlg9'

# Create a client instance
client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard
client.connect(THINGSBOARD_HOST, 1883, 60)

# Define telemetry data function
def send_telemetry_data():
    temperature = random.randint(0,100)
    humidity = random.randint(0,50)

    # Prepare telemetry data in JSON format
    telemetry_data = {
        "temperature": temperature,
        "humidity": humidity
    }

    # Convert telemetry data to JSON and send it to ThingsBoard
    client.publish('v1/devices/me/telemetry', json.dumps(telemetry_data), 1)

    print("Telemetry data sent:", telemetry_data)

try:
    while True:
        send_telemetry_data()
        time.sleep(1)  # Send telemetry data every 5 seconds

except KeyboardInterrupt:
    print("Program terminated by user.")
    client.disconnect()