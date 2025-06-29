import requests

response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
btc_price = response.json()["bitcoin"]["usd"]

print("Bitcoin Price (USD):", btc_price)
