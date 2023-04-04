import json

# MARK: Minify Functions

def minify_daily_weather_info(json_string, start_date=None, end_date=None):
    weather_data = json.loads(json_string)
    periods = weather_data["properties"]["periods"]

    if start_date and end_date:
        filtered_periods = [period for period in periods if start_date <= period["startTime"][:10] and end_date >= period["endTime"][:10]]
        condensed_periods = [extract_period_info(period) for period in filtered_periods]
    else:
        condensed_periods = [extract_period_info(period) for period in periods]

    condensed_weather_data = {"periods": condensed_periods}
    return json.dumps(condensed_weather_data, indent=2)

def minify_hourly_weather_info(json_string, start_date=None, end_date=None):
    weather_data = json.loads(json_string)
    periods = weather_data["properties"]["periods"]

    if start_date and end_date:
        filtered_periods = [period for period in periods if start_date <= period["startTime"] and end_date >= period["endTime"]]
        condensed_periods = [extract_hourly_period_info(period) for period in filtered_periods]
    else:
        condensed_periods = [extract_hourly_period_info(period) for period in periods]

    condensed_weather_data = {"periods": condensed_periods}
    return json.dumps(condensed_weather_data, indent=2)

# MARK: Helper Functions

def extract_period_info(period):
    return {
        "date": period["startTime"],
        "detailedForecast": period["detailedForecast"],
        "dewpoint": f"{period['dewpoint']['value']} {period['dewpoint']['unitCode'].split(':')[-1]}",
        "chanceOfPrecipitation": f"{period['probabilityOfPrecipitation']['value']} {period['probabilityOfPrecipitation']['unitCode'].split(':')[-1]}",
        "relativeHumidity": f"{period['relativeHumidity']['value']} {period['relativeHumidity']['unitCode'].split(':')[-1]}",
    }

def extract_hourly_period_info(period):
    return {
        "startDate": period["startTime"],
        "endDate": period["endTime"],
        "shortForecast": period["shortForecast"],
        "windSpeed": f"{period['windSpeed']} {period['windSpeed'].split()[-1]}",
        "windDirection": period["windDirection"],
        "temperature": f"{period['temperature']} {period['temperatureUnit']}",
        "dewpoint": f"{period['dewpoint']['value']} {period['dewpoint']['unitCode'].split(':')[-1]}",
        "chanceOfPrecipitation": f"{period['probabilityOfPrecipitation']['value']} {period['probabilityOfPrecipitation']['unitCode'].split(':')[-1]}",
        "relativeHumidity": f"{period['relativeHumidity']['value']} {period['relativeHumidity']['unitCode'].split(':')[-1]}",
    }