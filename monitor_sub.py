import time
import paho.mqtt.client as mqtt

## Function called when client connect to the broker

def on_connect( client , userdata, flags , rc):
    ## all the variables above, paho collects on its own
    ## since on_connect is a predefined variable it collects it on its own
    if rc == 0 : # when rc equals 0 the connection is accepted
        print("Successfully connected to broker")
        # Subscribing to a single level wilcard topic at Qos1
        # QoS1 = Gurantees at least one delivery
        client.subscribe("home/#" , qos=1)
        print("Subscribed to topic: home/#")
    else: # if connection failed
        print(f"Connection failed with code {rc}")

## Function called when a message is received from the broker
def on_message( client , userdata , msg ):
    payload = msg.payload.decode("utf-8")
    print(f"Received message : '{payload}' on topic: '{msg.topic}' (QoS): {msg.qos}")

## Create a client instance explicity engorcing MQTT 3.1.1
## Provide a unique client ID for persistent session tracking later
client = mqtt.Client(client_id="Pi_Monitor_Subscriber" , protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message 

## Connect to the local Mosquitto broker running on my local raspberry pi
client.connect("localhost" , 1883 , keepalive=60) ## how long before quiting subscription

## Start the network loop
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\nDisconnecting subscriber")
    client.disconnect()