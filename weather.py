import requests

def get_hko_forecast():
    
    base_url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php"
    
    params = {
        "dataType": "fnd", 
        "lang": "tc"        
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if "weatherForecast" in data:
            print(f"数据更新时间: {data.get('updateTime', '未知')}\n")
            
            for day in data["weatherForecast"]:
                date = day.get("forecastDate")
                weather = day.get("forecastWeather")
                min_temp = day.get("forecastMintemp", {}).get("value")
                max_temp = day.get("forecastMaxtemp", {}).get("value")
                if day.get("PSR") == "低" and max_temp < 30:
                    str = '適合行山'
                else:
                    str = '不適合行山'
                
                print(f"日期: {date}")
                print(f"天气: {weather}")
                print(f"温度: {min_temp}°C ~ {max_temp}°C")
                print(f"行動: {str}")
                print("-" * 30)
        else:
            print("未获取到预报数据，返回内容:", data)
            
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")

if __name__ == "__main__":
    get_hko_forecast()