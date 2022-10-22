import led
import config
import alert

from datetime import datetime
import time
import math

Alert = alert.Alert()

class Strikes():
  def __init__(self):
    self.strikes = []
    self.lastAlert = 'none'

  def new(self, time, lon, lat):
    # Check if the strike is already in the list with the exact same time, lon and lat
    for strike in self.strikes:
      if strike['time'] == time and strike['lon'] == lon and strike['lat'] == lat:
        return
      
    # Add the strike to the list
    self.strikes.append({
      'time': time,
      'lat': lat,
      'lon': lon,
      'distance': self.calculateCrow(lat, lon)
    })
    print("New lightning strike: " + str(datetime.fromtimestamp(int(time / 1000))) + " at " + str(lon) + ", " + str(lat) + " (Distance away: " + str(self.calculateCrow(lat, lon)) + "km)")

  def doCheck(self, currentTimestamp):
    self.timeFilter(currentTimestamp)
    self.checkIfClose()

  def timeFilter(self, currentTimestamp):
    # Filter out any strikes that are older than 15 minutes
    oldStrikesLength = len(self.strikes)
    self.strikes = [strike for strike in self.strikes if int(strike['time'] / 1000) > currentTimestamp - 60 * 15]

    # Print the number of strikes that were removed
    if oldStrikesLength != len(self.strikes):
      print("Removed " + str(oldStrikesLength - len(self.strikes)) + " strikes as they are older than 15 minutes.")

  def checkIfClose(self):
    if len(self.strikes) <= 0:
      print("All good... No strikes in the last 15 minutes.")
      return

    # Get the closest strike
    closestStrike = min(self.strikes, key=lambda x: x['distance'])

    # If closest strike is within 15km...
    if closestStrike['distance'] <= 15:
      Alert.doAlert('close', self.strikes)
    # If closest strike is within 30km...
    elif closestStrike['distance'] <= 30:
      Alert.doAlert('nearby', self.strikes)
    # If closest strike is over 30km away...
    else:
      Alert.clearAlert()

  def calculateCrow(self, lat, lon):
    R = 6371 # Radius of the earth in km
    dLat = self.toRad(lat - config.homeLat)
    dLon = self.toRad(lon - config.homeLon)
    hLat = self.toRad(config.homeLat)
    hLat = self.toRad(config.homeLon)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(hLat) * math.cos(hLat) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return round(d, 2)

  def toRad(self, deg):
    return deg * (math.pi/180)