import json
from datetime import datetime
import time

def error(reason, quit):
    while True:
        try:
            with open("running_resources\data\errors.json", "r") as f:
        

                try:
                    data= json.load(f)
                except json.JSONDecodeError:
                    with open("running_resources\data\errors.json", "w") as f:
                        json.dump({}, f)
                    with open("running_resources\data\errors.json", "r") as f:
                        data= json.load(f)
                if quit == True:
                    data["stop_excecutor"] = 'True'
                if quit == False:
                    data["stop_excecutor"] = 'False'
                try:
                    error_num_raw = list(data['error'].keys())[-1]
                    error_num_raw_stringed = error_num_raw.replace("[", "").replace("]", "").replace('"', "")
                    error_num_stripped = error_num_raw_stringed.split("_")
                    error_num = int(error_num_stripped[1])
                    data["error"][f"error_{error_num+1}"] = {
                        "reason": reason,
                        "timestamp": str(datetime.now())
                }
                except IndexError:
                    data["error"]["error_1"] = {
                    "reason": reason,
                    "timestamp": str(datetime.now())
                }
                except KeyError:
                    data["error"]= {"error_1" : {"reason": reason, "timestamp" : str(datetime.now())}}
                    
                
                    
            with open("running_resources\data\errors.json", "w") as f:
                json.dump(data, f, indent=4)
            break
        except FileNotFoundError:
            with open("running_resources\data\errors.json", "w") as f:
                continue
start = time.time()
end= time.time()
print(end-start)