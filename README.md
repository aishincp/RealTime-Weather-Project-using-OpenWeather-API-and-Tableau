# Real-Time Weather Dashboard using OpenWeather API, Google Sheets, and Tableau

### Introduction
I am expanding my skill set by integrating API interfacing into a practical project, which is essential for accessing real-time data.

### Aim

- Build a real-time weather dashboard.
- Fetch weather data using the OpenWeather API.
- Store and update data in Google Sheets.
- Visualize the data using Tableau Public.
- By completing this project, enhanced my API interfacing skills and created a dashboard that provides real-time weather insights.

### Project Planning and Execution

##### 1. Objective
Create a real-time, interactive weather dashboard that:

- Fetches current weather and 5-day forecast data at 3-hour intervals.
- Updates the data in real time.
- Visualizes the data in an accessible and user-friendly format.
  
##### 2. Tools and Technologies
- Python: For API calls and data handling.
- OpenWeather API: Source of real-time weather data.
- Google Sheets: Acts as a live data source.
- gspread Library: Python library to interact with Google Sheets.
- Tableau Public: For data visualization and dashboard creation.
- Google Cloud Platform: This is used to set up Google Sheets API credentials.

### Procedure
##### 1. Registering with OpenWeather API
- Signup: Created an account on [OpenWeather](https://openweathermap.org/) to obtain an API key.
- API Key: Received free API key for accessing weather data (limited access only)

##### 2. Importing relevant libraries

```
import requests
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
```

##### 3. Fetching Weather Data
*Code Overview*:

```
# API details
api_key = "7bed05cd21df6beef2392982fa1f9c8f"

# Location
city = 'Frankfurt'

# API endpoint urls
current_weather_url = 'https://api.openweathermap.org/data/2.5/weather'
forecast_url = 'https://api.openweathermap.org/data/2.5/forecast'

# Get Current Weather Data
def get_current_weather_data(city, api_key):
    params = {
        'q': city,
        'appid' : api_key,
        'units': 'metric'  # for Celsius
    }
    response = requests.get(current_weather_url, params=params)
    return response.json()

# Get Forecast Data
def get_forecast_data(city, api_key):
    params = {
        'q': city,
        'appid' : api_key,
        'units': 'metric'  # for Celsius
    }
    response = requests.get(forecast_url, params=params)
    return response.json()

weather_data = get_current_weather_data(city, api_key)
forecast_data = get_forecast_data(city, api_key)
```

__NOTE:__ In the above code, two things are most importantly done:
- a. Requesting library which are used to make __HTTP requests__ to API endpoints.
- b. __JSON parsing__ for API responses to extract relevant data

### Setting Up Google Sheets API
1. Created **Google Cloud Project** in the Google Cloud Console.
2. Enable **Google Sheets APIs** and **Google Drive API**.
3. Created a **Service Account** and also credentials.json file.
4. Created a Google Sheet named **"WeatherAPI"** and shared it with the service account email.

Below is the code for **Authentication of Google sheets**:
```
# Google Sheets authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
json_key_file_path = "path_to_your_credentials.json"
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_key_file_path, scope)
client = gspread.authorize(credentials)
```

### Fetching Data to Google Spreadsheet

- __Current Weather Data__:
```
weather_row = [
    weather_data['name'],
    f"{weather_data['main']['temp']:.2f}",  
    f"{weather_data['main']['humidity']}",   
    f"{weather_data['wind']['speed']}",   
    weather_data['weather'][0]['description'],
    weather_data['dt']
]
```

- __Forecast Weather Data__:
```
forecast_rows = []
for forecast in forecast_data['list']:
    forecast_row = [
        forecast['dt_txt'],
        f"{forecast['main']['temp']:.2f}",   
        f"{forecast['main']['humidity']}",    
        f"{forecast['wind']['speed']}",    
        forecast['weather'][0]['description']
    ]
    forecast_rows.append(forecast_row)
```

- __Writing to Sheets__:
```
# Accessing Google Sheet
spreadsheet = client.open("WeatherAPI")
current_data_sheet = spreadsheet.worksheet("CurrentData")
forecast_sheet = spreadsheet.worksheet("ForecastData")

# Inserting current and forecast weather data in separate sheets
current_data_sheet.append_row(weather_row)
forecast_sheet.append_row(forecast_row)
```

### Data Visualization with Tableau
- Connecting Google Sheets to Tableau
- Preparing Data in Tableau (Ensured **Data Types** and **Date Parsing**)
- Creating Worksheet Visuals and Dashboard Layout

### Results
The final dashboard displays:

- Current Weather Conditions: Temperature, humidity, wind speed, and weather description.
- 5-Day Forecast: Trends at 3-hour intervals.
- Interactive Visuals: Users can interact with the chart to see specific data points.



[Tableau Dashboard Link](https://public.tableau.com/app/profile/aishin.abdulla.yoosufali/viz/WeatherData_17256697822640/WeatherDashboard?publish=yes)
