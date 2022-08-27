from pybit.inverse_perpetual import HTTP
from config_secret import API_SECRET
from config_secret import API
import json

with open("running_resources\created_session\settings_secret.json", "r") as f:
    data = json.load(f)
    
API = data["API"]
API_SECRET = data['API_SECRET']



session = HTTP("https://api.bybit.com",
               api_key=API, api_secret=API_SECRET)
