from time import sleep
import paho.mqtt.client as mqtt

###################################
# Graphics imports, constants and structures
###################################
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw

# this is the size of ONE of our matrixes. 
matrix_rows = 32
matrix_columns = 32

# how many matrixes stacked horizontally and vertically 
matrix_horizontal = 5
matrix_vertical = 3

total_rows = matrix_rows * matrix_vertical
total_columns = matrix_columns * matrix_horizontal

options = RGBMatrixOptions()
options.rows = matrix_rows 
options.cols = matrix_columns 
options.chain_length = matrix_horizontal
options.parallel = matrix_vertical 
options.hardware_mapping = 'regular'  
options.gpio_slowdown = 2

matrix = RGBMatrix(options = options)

_shutdown = False
_saw_camera = False

def display_jpg():
  global matrix

  image = Image.open("temp.jpg").convert('RGB')
  image = image.resize((total_columns,total_rows))
  image = image.transpose(Image.FLIP_LEFT_RIGHT)
  matrix.SetImage(image, 0, 0)

# message handling callback 
def on_message(client, userdata, message):
  global _shutdown
  global _saw_camera
  
  if message.payload == "imageDone":
    _saw_camera = True
    print "imageDone received.  Displaying picture"
    display_jpg()
    print "sending displayReady"
    client.publish("camera", "displayReady")
  if message.topic == "shutdown":
    print("received shutdown message");
    _shutdown = True
    
# MAIN CODE
broker_address="mqttbroker"
client = mqtt.Client("camera_display")
client.on_message=on_message
client.connect(broker_address)
client.loop_start()
client.subscribe("camera")
client.subscribe("shutdown")
print "display running."

while (_saw_camera == False):
  print "sending displayReady"
  client.publish("camera", "displayReady")
  sleep(1)

try:
  print("Press CTRL-C to stop")
  while True:
    if (_shutdown == True):
      exit(0)
    sleep(1)
except KeyboardInterrupt:
  exit(0)

