import requests

url = "http://api.open-notify.org/iss-now.json"

response = requests.get(url=url)

data = response.json()

print(data['iss_position']['latitude'])
