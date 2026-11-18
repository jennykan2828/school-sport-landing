from flask import Flask, jsonify, render_template
import requests
import random


app = Flask(__name__)
url = "http://api.open-notify.org/iss-now.json"
base_url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php"
params = {
    "dataType": "fnd",
    "lang": "tc"
}

@app.route('/')
def home():
    # return '<h1>hello world</h1>'
    mymood = random.choice(['happy', 'delightful', 'excited'])
    person = {'face':'handsome', 'age':25}
    return render_template('index.html', mood = mymood, person=person)

@app.route('/kitty/')
def khome():
    return '<h1>hello kitty</h1>'

@app.route('/spaceapi/')
def space():
    response = requests.get(url=url)
    data = response.json()
    latitude = data['iss_position']['latitude']
    longitude = data['iss_position']['longitude']
    location_dict = {'long':longitude, 'lat': latitude}
    return render_template('space.html', locate = location_dict )

@app.route('/frankie/')
def showFrankie():
    frankie = {'name': 'frankie', 'face':'hansome'}
    return jsonify(frankie)

@app.route('/weather/')
def showweather():
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "weatherForecast" not in data:
            return {"error": "未获取到预报数据", "days": []}

        days = []
        for day in data["weatherForecast"]:
            date = day.get("forecastDate")
            weather = day.get("forecastWeather")
            min_temp = day.get("forecastMintemp", {}).get("value")
            max_temp = day.get("forecastMaxtemp", {}).get("value")
            psr = day.get("PSR")
            week = day.get("week")

            # Your original logic
            if psr == "低" and max_temp is not None and max_temp < 30:
                action = "適合行山"
                suitable = True
            else:
                action = "不適合行山"
                suitable = False

            # Nice date format: 20261105 → 11月5日
            nice_date = date
            if date and len(date) == 8:
                nice_date = f"{date[4:6]}月{int(date[6:8])}日"

            days.append({
                "date": nice_date,
                "week": week,
                "weather": weather,
                "min_temp": min_temp,
                "max_temp": max_temp,
                "psr": psr,
                "action": action,
                "suitable": suitable
            })

        # return {
        #     "updateTime": data.get("updateTime"),
        #     "days": days,
        #     "error": None
        # }

    except requests.exceptions.RequestException as e:
        print( {
            "error": f"请求失败: {str(e)}",
            "days": [],
            "updateTime": None
        })
    return render_template('weather.html', days = days )

if __name__ == '__main__':
    app.run(debug=True, port= 5500)