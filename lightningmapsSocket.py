import config
import strikes

import json
import websocket

try:
  import RPi.GPIO as GPIO
  hasGPIO = True
except (ImportError, RuntimeError):
  hasGPIO = False


# Create a new instance of the Strikes class
Strikes = strikes.Strikes()


def on_message(ws, message):
  jsonparse = json.loads(message)
  """
    The jsonparse returns two main things...
    1. 'time' - a int value of the last time the data was updated
    2. 'strokes' - (sometimes) a list of lightning strikes. Each strike has a 'time', 'lon' and 'lat' value.
    
    The 'strokes' list is sometimes there, sometimes not and sometimes empty.
  """
  # Check if the 'strokes' key exists
  if 'strokes' in jsonparse:
    # Loop through each stroke and just get the 'time', 'lon' and 'lat' values
    for stroke in jsonparse['strokes']:
      Strikes.new(int(stroke['time']), float(stroke['lon']), float(stroke['lat']))

  # Check if the 'time' key exists
  if 'time' in jsonparse:
    Strikes.doCheck(int(jsonparse['time']))

def on_error(ws, error):
  print("[ws] Error:")
  print(error)

def on_close(ws, reason, code):
  print("[ws] Closed connection.")
  if hasGPIO: GPIO.cleanup()
  print("[info] GPIO cleaned up.")

def on_open(ws):
  print("[ws] Connection established.")
  # TODO: I need to figure out how to make this work with the homeLat and homeLon values from config.py, this is based on the view of where I live...
  ws.send('{"v":24,"i":{"1":31224637,"2":38259244},"s":true,"x":0,"w":0,"tx":0,"tw":0,"a":4,"z":11,"b":true,"h":"#y=' + str(config.homeLon) + ';x=' + str(config.homeLat) + ';z=9;d=9;dl=3;dc=0;t=3;o=0;","l":3460,"t":1666331401,"from_lightningmaps_org":true,"r":"v"}')

def start():
  # websocket.enableTrace(True)
  ws = websocket.WebSocketApp("wss://live.lightningmaps.org/",
    on_message = on_message,
    on_error = on_error,
    on_close = on_close
  )

  ws.on_open = on_open

  ws.run_forever()