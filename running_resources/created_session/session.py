from pybit.inverse_perpetual import HTTP
import json
with open("running_resources\created_session\settings_secret.json", "r") as f:
    data = json.load(f)
    
API = data["API"]
API_SECRET = data['API_SECRET']



session = HTTP("https://api.bybit.com",
               api_key=API, api_secret=API_SECRET)
