from flask import Flask, render_template
import requests

app = Flask(__name__)

# HKO 9-day forecast API (English)
API_URL = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang=en"

@app.route('/')
def index():
    try:
        resp = requests.get(API_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        return f"Failed to fetch weather data: {e}"

    forecast_list = data.get('weatherForecast', [])

    # Build list of dicts for the template
    rows = []
    for day in forecast_list:
        rows.append({
            'date': day.get('forecastDate', ''),
            'week': day.get('week', ''),
            'weather': day.get('forecastWeather', ''),
            'max_temp': day.get('forecastMaxtemp', {}).get('value', ''),
            'min_temp': day.get('forecastMintemp', {}).get('value', ''),
            'icon': day.get('ForecastIcon', ''),
        })

    return render_template('index.html', rows=rows)


@app.route('/weatherbs')
def weatherbs():
    try:
        resp = requests.get(API_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        return f"Failed to fetch weather data: {e}"

    forecast_list = data.get('weatherForecast', [])

    # Build list of dicts for the template
    rows = []
    for day in forecast_list:
        rows.append({
            'date': day.get('forecastDate', ''),
            'week': day.get('week', ''),
            'weather': day.get('forecastWeather', ''),
            'max_temp': day.get('forecastMaxtemp', {}).get('value', ''),
            'min_temp': day.get('forecastMintemp', {}).get('value', ''),
            'icon': day.get('ForecastIcon', ''),
        })

    return render_template('weather-bootstrap.html', rows=rows)


if __name__ == '__main__':
    app.run(debug=True)