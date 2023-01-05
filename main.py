from flask import Flask
from flask import render_template
from flask import request

import requests
from datetime import datetime
import math

app = Flask("Flask App")

@app.route('/')
def index():

    weather_data = {
        'lat': '-',
        'lon': '-',
        'name': '-',
        'description': '-',
        'temp': '-',
        'date': '-',
        'time': '-',
        "wind": '-',
        "sunrise": '-',
        "sunset": '-',
        "humidity": '-',
        "visibility": '-'
    }

    air_data = {
        'aqi': '-'
    }

    return render_template('index.html', data = weather_data, air = air_data)

@app.route('/<city>', methods=['GET'])
def get_weather_data(city=None):

    app_key = "97afc2cc2288a1a21346dc87f8fe2f13"

    try:
        api_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={app_key}").json()
        weather_data = {
            'lat': api_data['coord']['lat'],
            'lon': api_data['coord']['lon'],
            'name': api_data['name'],
            'description': api_data['weather'][0]['main'] + ' - ' + api_data['weather'][0]['description'],
            'temp': math.trunc(api_data['main']['temp'] - 273.15),
            'date': datetime.fromtimestamp(api_data['dt']).strftime('%A, %b %d'),
            'time': datetime.fromtimestamp(api_data['dt']).strftime("%H:%M"),
            "wind": api_data['wind']['speed'],
            "sunrise": datetime.fromtimestamp(api_data['sys']['sunrise']).strftime("%I:%M %p"),
            "sunset": datetime.fromtimestamp(api_data['sys']['sunset']).strftime("%I:%M %p"),
            "humidity": api_data['main']['humidity'],
            "visibility": api_data['visibility'] / 1000
        }

        api_data = requests.get(f"http://api.openweathermap.org/data/2.5/air_pollution?lat={weather_data['lat']}&lon={weather_data['lon']}&appid={app_key}").json()
        air_data = {
            'aqi': api_data['list'][0]['main']['aqi']
        }
    except:
        weather_data = {
                'lat': '-',
                'lon': '-',
                'name': '-',
                'description': '-',
                'temp': '-',
                'date': '-',
                'time': '-',
                "wind": '-',
                "sunrise": '-',
                "sunset": '-',
                "humidity": '-',
                "visibility": '-'
            }

        air_data = {
            'aqi': '-'
        }

    return render_template('index.html', data = weather_data, air = air_data)