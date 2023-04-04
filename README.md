# NWS Weather Plugin

A plugin for ChatGPT to get access to free weather data for locations in the US through the NWS. 

This is a development plugin, and mostly consists of a flask app that has to be run locally in order to use. You must already have plugin access from OpenAI.

The server is essentially a proxy to the NWS's official API here (https://www.weather.gov/documentation/services-web-api#/). The reason a proxy is useful here is the NWS returns pretty lengthy responses in their official API. This prunes and minifies these responses down so that they're easily digestible by chatGPT (and so you dont run into context length issues).

## Supported Endpoints:

- [x] Daily Weather Forecast
- [x] Hourly Weather Forecast (note: don't request more than 24 hours of data, otherwise you run into context length problems)
- [x] Multi City Forecast (to get weather about multiple cities in one request instead of multiple)

## Up Next:

- [ ] Active Weather Alerts

## Running Locally
1. `python3.9 pip install -r requirements.txt`

2. `python3.9 app/server.py`

It'll be active on `localhost:3333`.
