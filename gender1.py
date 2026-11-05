import requests

params = {'name':'peter'}
url = 'https://api.genderize.io'
urlcoin = 'https://data-api.binance.vision/api/v3/ticker/price'
coin_params = {'symbol':'ETHBTC'}


result = requests.get(url=url, params = params)
print(result.json())
coin_result = requests.get(url=urlcoin, params = coin_params)
print(coin_result.json())