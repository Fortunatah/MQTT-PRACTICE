## this is my basic publisher
import time
import os
import paho.mqtt.client as mqtt

# Helper function to read the Raspberry Pi's actual CPU temperature
def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_raw = int(f.read())
        return round(temp_raw / 1000.0, 1)  # Convert millidegrees to Celsius
    except FileNotFoundError:
        return 25.0  # Fallback mock temperature if not running on a Pi

## Create a client instance enforcing MQTT 3.1.1
client = mqtt.Client(client_id="Pi_temp_publisher" , protocol=mqtt.MQTTv311 )

## Configure last will and testament
client.will_set(
    topic="home/living_room/status",
    payload="offline",
    qos=1,
    retain=True
)
## Connecting to the local broker
print("Connecting publisher to local broker...")
client.connect("localhost" , 1883, keepalive=60)

client.loop_start()
print("Publisher is running. Press Ctrl+C to stop.")
# Right after connecting, let everyone know we are alive and well
client.publish("home/living_room/status", payload="online", qos=1, retain=True)
try:
    while True:
        ## get the current cpu temperature from above
        cpu_temp = get_cpu_temp()
        topic = "home/living_room/temperature"
        payload = str(cpu_temp)

        print(f"Publishing: {payload} to topic: {topic}")

        ## Publish this message at Qos1 (At least once delivery)
        client.publish(topic, payload=payload, qos=1, retain=False)
        # Wait 5 seconds before the next reading
        time.sleep(5)

except KeyboardInterrupt:
    print("\nStopping publisher...")
    client.loop_stop()
    client.disconnect()
