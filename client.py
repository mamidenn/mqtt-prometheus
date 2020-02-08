import paho.mqtt.client as mqtt
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("hab/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))    
    if(msg.topic == 'hab/livingroom/temperature'):        
        t.set(float(msg.payload))
    if(msg.topic == 'hab/livingroom/humidity'):        
        h.set(float(msg.payload))
    push_to_gateway('rasputin:32768', job='livingroom', registry=registry)

    

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("rasputin", 1883, 60)

registry = CollectorRegistry()
t = Gauge('temperature', 'Current temperature', registry=registry)
h = Gauge('humidity', 'Current humididty', registry=registry)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()