import json
import gspread
import time, string
import pyowm

from sense_hat import SenseHat
from oauth2client.client import GoogleCredentials

# Connect to senseHat
sense = SenseHat()
sense.low_light = True
# display on sesnse HAT script start
# R - reading sensors
sense.show_letter("R")

# SenseHat sensor readings
pressure = sense.get_pressure()
humidity = sense.get_humidity()
temperature = sense.get_temperature()

# read actual weather from openweathermap. You need a API Key from OpenWeatherMap
owm = pyowm.OWM('API_key_here')

observation = owm.weather_at_place('Timisoara,ro')
w = observation.get_weather()
wind=w.get_wind()                  # {'speed': 4.6, 'deg': 330}
Whumid=w.get_humidity()              # 87
temp=w.get_temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min'
Wstatus= w.get_status()
Wwind = wind.get('speed')
Wtemp = temp.get('temp')

#open google sheet senseHAT
credentials = GoogleCredentials.get_application_default()
credentials = credentials.create_scoped(['https://spreadsheets.google.com/feeds'])


gc = gspread.authorize(credentials)
gc = gspread.authorize(credentials)

# You'll need a Google Doc Key 
wks = gc.open_by_key('Google_Doc_key').sheet1
ip_time = time.strftime('%I:%M%p')
ip_date = time.strftime('%m/%d/%y')

values = [ip_date, ip_time, pressure, humidity, temperature, Wstatus, Wwind, Wtemp, Whumid]

wks.append_row(values)

# write on senseHat the end of readings & google doc update
sense.show_message("OK", text_colour=[255, 0, 0])
sense.clear()


