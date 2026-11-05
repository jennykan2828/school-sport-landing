import requests

urlcoin = 'https://data-api.binance.vision/api/v3/ticker/price'
coin_params = {'symbol':'ETHBTC'}


coin_result = requests.get(url=urlcoin, params = coin_params)
print(coin_result.json())
print(coin_result.json())
