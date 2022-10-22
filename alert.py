import config
import led

from datetime import datetime
from discord_webhook import DiscordWebhook
from staticmap import StaticMap, CircleMarker

LED = led.LED()

class Alert():
  def __init__(self):
    self.lastAlert = 'none'

  def doAlert(self, type, strikes):
    if self.lastAlert != type:
      self.lastAlert = type

      closestStrike = min(strikes, key=lambda x: x['distance'])

      # If the closest strike is within 15km
      if type == 'close':
        print(" ------------------------------------------------------------------")
        print("| !!!! CLOSE !!!!  Lightning strike within 15km of your location. |")
        print(("| Distance: " + str(closestStrike['distance']) + "km @ " + str(datetime.fromtimestamp(int(closestStrike['time'] / 1000)))).ljust(67) + "|")
        print(" ------------------------------------------------------------------")
        
        # Send Discord alert
        self.createDiscordMessage('close', strikes)

        # Set LED to red
        LED.red(True)
        LED.yellow(False)
        LED.green(False)

      # If the closest strike is within 30km
      elif type == 'nearby':
        print(" ------------------------------------------------------------------")
        print("| !!!! CLOSE !!!!  Lightning strike within 15km of your location. |")
        print(("| Distance: " + str(closestStrike['distance']) + "km @ " + str(datetime.fromtimestamp(int(closestStrike['time'] / 1000)))).ljust(67) + "|")
        print(" ------------------------------------------------------------------")
        
        # Send Discord alert
        self.createDiscordMessage('nearby', strikes)

        # Set LED to red
        LED.red(False)
        LED.yellow(True)
        LED.green(False)

  # Send a Discord alert that the lightning has passed
  def clearAlert(self):
    if config.discordWebhookUrl == '':
      return

    if self.lastAlert != 'none':
      self.lastAlert = 'none'
      DiscordWebhook(url=config.discordWebhookUrl, content="Lightning passed... There has not been any lighting nearby for the past 15 minutes.").execute()

  # Creates a Discord alert of the lighting strikes and the status along with a map with markers of the strikes
  def createDiscordMessage(self, type, strikes):
    if config.discordWebhookUrl == '':
      return

    nearbyStrikes = [strike for strike in strikes if strike['distance'] > 15 and strike['distance'] <= 30]
    closeStrikes = [strike for strike in strikes if strike['distance'] <= 15]
    closestStrike = min(strikes, key=lambda x: x['distance'])

    # Create the message body
    # messageTitle = '@everyone'
    messageTitle = ''
    distanceType = ''
    if (type == 'close'):
      messageTitle += ' ⚠ **Lightning CLOSE** ⚠'
      distanceType = '15km'
    elif (type == 'nearby'):
      messageTitle += ' **Lightning nearby**'
      distanceType = '30km'
    messageBody = f'{messageTitle}\nThere was a lightning strike within {distanceType} of the house...\n`Distance: ' + str(closestStrike['distance']) + 'km @ ' + str(datetime.fromtimestamp(int(closestStrike['time'] / 1000))) + '`'

    # Create the map
    map = StaticMap(600, 600, 10, 10)

    # Add markers for the strikes
    for strike in nearbyStrikes:
      map.add_marker(CircleMarker((strike['lon'], strike['lat']), '#ffff00', 5))
    
    for strike in closeStrikes:
      map.add_marker(CircleMarker((strike['lon'], strike['lat']), '#ff0000', 5))
    
    map.add_marker(CircleMarker((config.homeLon, config.homeLat), 'blue', 10))

    # Save the map to a file
    mapImage = map.render()
    mapImage.save('map.png')

    # Create the Webhook content
    webhook = DiscordWebhook(url=config.discordWebhookUrl, content=messageBody)

    # Attach the map to the message
    with open('map.png', 'rb') as f:
      webhook.add_file(file=f.read(), filename='map.png')
    
    webhook.execute()
