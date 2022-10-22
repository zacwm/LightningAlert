import config

try:
  import RPi.GPIO as GPIO
  hasGPIO = True
except (ImportError, RuntimeError):
  hasGPIO = False

class LED():
  def __init__(self):
    if hasGPIO:
      GPIO.setmode(GPIO.BCM)
      GPIO.setwarnings(False)

      GPIO.setup(config.greenPin, GPIO.OUT)
      GPIO.setup(config.yellowPin, GPIO.OUT)
      GPIO.setup(config.redPin, GPIO.OUT)

  def green(self, state):
    if hasGPIO:
      if state:
        GPIO.output(config.greenPin, GPIO.HIGH)
      else:
        GPIO.output(config.greenPin, GPIO.LOW)

  def yellow(self, state):
    if hasGPIO:
      if state:
        GPIO.output(config.yellowPin, GPIO.HIGH)
      else:
        GPIO.output(config.yellowPin, GPIO.LOW)

  def red(self, state):
    if hasGPIO:
      if state:
        GPIO.output(config.redPin, GPIO.HIGH)
      else:
        GPIO.output(config.redPin, GPIO.LOW)
