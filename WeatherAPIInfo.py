import requests
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# API key details
api_key = "7bed05cd21df6beef2392982fa1f9c8f"

# Location
city = 'Frankfurt'

# API endpoint urls
current_weather_url = 'https://api.openweathermap.org/data/2.5/weather'
forecast_url = 'https://api.openweathermap.org/data/2.5/forecast'

# extracting current weather data
def get_current_weather_data(city, api_key):
    params = {
        'q': city,
        'appid' : api_key,
        'units': 'metric'  # for Celsius
    }
    response = requests.get(current_weather_url, params=params)
    return response.json()

# extracting forecast weather data for next consecutive 5 days
def get_forecast_data(city, api_key):
    params = {
        'q': city,
        'appid' : api_key,
        'units': 'metric'  # for Celsius
    }
    response = requests.get(forecast_url, params=params)
    return response.json()

# Calling functions
weather_data = get_current_weather_data(city, api_key)
forecast_data = get_forecast_data(city, api_key)

# Google sheets authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# path to JSON key file
json_key_file_path = r"C:\Users\yousuf\source\DataAnalysisProjects\WeatherAPI\credentials.json"

# authentication and client creation
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_key_file_path, scope)
client = gspread.authorize(credentials)

# Accessing Google Sheet
spreadsheet = client.open("WeatherAPI")
current_data_sheet = spreadsheet.worksheet("CurrentData")
forecast_sheet = spreadsheet.worksheet("ForecastData")

# Data preparation to insert current weather data
weather_row = [
    weather_data['name'],
    f"{weather_data['main']['temp']:.2f}°C",  
    f"{weather_data['main']['humidity']}%",   
    f"{weather_data['wind']['speed']} m/s",   
    weather_data['weather'][0]['description'],
    weather_data['dt']
]

current_data_sheet.append_row(weather_row)

# Inserting forecast data into another worksheet 
for forecast in forecast_data['list']:
    forecast_row = [
        forecast['dt_txt'],
        f"{forecast['main']['temp']:.2f}°C",   
        f"{forecast['main']['humidity']}%",    
        f"{forecast['wind']['speed']} m/s",    
        forecast['weather'][0]['description']
    ]
    forecast_sheet.append_row(forecast_row)
