from pybit.unified_trading import HTTP
import json
with open("running_resources\created_session\settings_secret.json", "r") as f:
    data = json.load(f)
    
API = data["API"]
API_SECRET = data['API_SECRET']



session = HTTP(api_key=API, api_secret=API_SECRET)
