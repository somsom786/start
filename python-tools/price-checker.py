import requests

response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd")
data = response.json()

print("Bitcoin Price (USD):", data["bitcoin"]["usd"])
print("Ethereum Price (USD):", data["ethereum"]["usd"])
