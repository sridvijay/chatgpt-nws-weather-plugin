import requests
import os

import yaml
from flask import Flask, jsonify, Response, request, send_from_directory
from flask_cors import CORS

from typing import List
from utils import *

app = Flask(__name__)

PORT = 3333

# Note: Setting CORS to allow chat.openapi.com is required for ChatGPT to access your plugin
CORS(app, origins=[f"http://localhost:{PORT}", "https://chat.openai.com"])

api_url = 'https://api.weather.gov'

@app.route('/.well-known/ai-plugin.json')
def serve_manifest():
    return send_from_directory(os.path.dirname(os.path.dirname(__file__)), 'ai-plugin.json')

@app.route('/openapi.yaml')
def serve_openapi_json():
    return send_from_directory(os.path.dirname(os.path.dirname(__file__)), 'openapi.yaml')

@app.route('/forecast/<lat>,<lon>')
def forecast_endpoint(lat, lon):
    # Build URL for metadata request
    metadata_url = f"https://api.weather.gov/points/{lat},{lon}"

    # Retrieve metadata
    metadata_response = requests.get(metadata_url)
    metadata = metadata_response.json()

    # Extract URL for forecast from metadata
    forecast_url = metadata['properties']['forecast']

    # Retrieve forecast
    forecast_response = requests.get(forecast_url)
    minified_daily_forecast = minify_daily_weather_info(forecast_response.text)

    return minified_daily_forecast

@app.route('/multi_city_forecast', methods=['POST'])
def multi_city_forecast_endpoint():
    # Check if the request has a JSON body
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    # Extract the coordinates array from the request JSON body
    coordinates = request.json.get('coordinates')

    # Validate the coordinates
    if not coordinates or not isinstance(coordinates, list):
        return jsonify({"error": "Invalid or missing 'coordinates' in JSON body"}), 400

    # Initialize list to hold weather data for each city
    forecasts = []

    # Loop through each set of coordinates and retrieve weather data for each city
    for coordinate in coordinates:
        lat, lon = coordinate['lat'], coordinate['lng']
        
        # Build URL for metadata request
        metadata_url = f"https://api.weather.gov/points/{lat},{lon}"

        # Retrieve metadata
        metadata_response = requests.get(metadata_url)
        metadata = metadata_response.json()

        # Extract URL for forecast from metadata
        forecast_url = metadata['properties']['forecast']

        # Retrieve forecast
        forecast_response = requests.get(forecast_url)
        minified_daily_forecast = minify_daily_weather_info(forecast_response.text)

        # Add weather data to list
        forecasts.append({'lat': lat, 'lon': lon, 'forecast': minified_daily_forecast})

    # Return list of weather data for each city
    return {'forecasts': forecasts}

@app.route('/forecastHourly/<lat>,<lon>')
def forecast_hourly_endpoint(lat, lon):
    # Build URL for metadata request
    metadata_url = f"https://api.weather.gov/points/{lat},{lon}"

    # Retrieve metadata
    metadata_response = requests.get(metadata_url)
    metadata = metadata_response.json()

    # Extract URL for hourly forecast from metadata
    forecast_hourly_url = metadata['properties']['forecastHourly']

    # Extract start and end dates from query parameters, if provided
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Retrieve hourly forecast
    forecast_hourly_response = requests.get(forecast_hourly_url)
    minified_hourly_forecast = minify_hourly_weather_info(forecast_hourly_response.text, start_date=start_date, end_date=end_date)

    return minified_hourly_forecast

@app.route('/logo.png')
def serve_icon():
    return send_from_directory(os.path.dirname(os.path.dirname(__file__)), 'icon.png')

if __name__ == '__main__':
    app.run(port=PORT)