# The camera side listens to the "camera" channel.  On displayReady, it stores
# a jpeg for the "display" side, and sends an "imageDone"

import paho.mqtt.client as mqtt
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (160,96)

def take_picture():
  global camera
  camera.capture("temp.jpg")

# message handling callback 
def on_message(client, userdata, message):
  global _shutdown
  
  if message.topic == "shutdown":
    print("shutdown received")
    _shutdown = True
    
  if message.payload == "displayReady":
    print "ready received.  Storing picture"
    take_picture()
    print "sending imageDone"
    client.publish("camera", "imageDone")

_shutdown = False
broker_address="mqttbroker"
client = mqtt.Client("camera")
client.on_message=on_message
client.connect(broker_address)
client.loop_start()
client.subscribe("camera")
client.subscribe("shutdown")

print "camera running."
while True:
  if (_shutdown == True):
    exit(0)
  time.sleep(1)
client.loop_stop()
