# The camera side listens to the "camera" channel.  On displayReady, it stores
# a jpeg for the "display" side, and sends an "imageDone"

import paho.mqtt.client as mqtt
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (64,64)

def take_picture():
  global camera
  camera.capture('temp.jpg')

# message handling callback 
def on_message(client, userdata, message):
  if message.payload == "displayReady":
    print "ready received.  Storing picture"
    take_picture()
    print "sending imageDone"
    client.publish("camera", "imageDone")

broker_address="10.0.0.17"
client = mqtt.Client("camera")
client.on_message=on_message
client.connect(broker_address)
client.loop_start()
client.subscribe("camera")
print "camera running."
while True:
  time.sleep(1)
client.loop_stop()
