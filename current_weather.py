import requests
import os
from dotenv import load_dotenv
import json
import time

def get_location():
    while True:
        file = open('location.txt', 'r')
        location = file.read()
        if location:
            return location
    
def get_lat_lon(location):
    WEATHER_API_KEY=os.getenv('WEATHER_API_KEY')
    details = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={location}&appid={WEATHER_API_KEY}')
    json_details = details.json()
    # print(json_details)
    latitude=json_details[0].get('lat')
    longitude=json_details[0].get('lon')
    # print(latitude, longitude)
    return latitude, longitude

def kelvin_to_fahrenheit(temp_kelvin):
    return (temp_kelvin - 273.15) * 9/5 + 32

def get_weather():
    weather_data = []
    location = get_location()
    print(location)
    latitude, longitude = get_lat_lon(location)
    WEATHER_API_KEY=os.getenv('WEATHER_API_KEY')
    details = requests.get(f'https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&appid={WEATHER_API_KEY}')
    json_details = details.json()

    
    current_temp_kelvin = json_details.get('current').get('temp')
    current_temp_fahrenheit = round(kelvin_to_fahrenheit(current_temp_kelvin),1)
    weather_data.append({'current_temp_fahrenheit': current_temp_fahrenheit})
    
    humidity = json_details.get('current').get('humidity')
    weather_data.append({'humidity': humidity})
    
    description = json_details.get('current').get('weather')[0].get('description')
    weather_data.append({'description': description})
    
    icon = json_details.get('current').get('weather')[0].get('icon')
    weather_data.append({'icon': icon})
    
    with open('data.json', 'w') as weather:
        json.dump(weather_data, weather)
        
    return weather_data
    
while True:
    time.sleep(2)
    get_weather()
    break