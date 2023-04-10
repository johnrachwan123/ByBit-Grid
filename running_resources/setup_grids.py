import json
from .data.config import UPPERLIMIT
from .data.config import LOWERLIMIT
from .data.config import GRIDS
from .data.config import MIN_PERC
from termcolor import colored
from .data.error_handle import error

# needs to check if it is a json for grids.json because sometimes some people just delete the {}
def grid(currentprice):

    print(colored("setting up grid", "yellow"))
    if UPPERLIMIT > LOWERLIMIT:

        if currentprice < UPPERLIMIT:

            if currentprice > LOWERLIMIT:

                range_btc = UPPERLIMIT - LOWERLIMIT
                level_price = range_btc/GRIDS
                level_percentage = (level_price/range_btc)*100

                if MIN_PERC > level_percentage:
                    print(colored(
                        f'percentage gain per level is under the minimal percentage wanted: {level_percentage}', "red"))

                    error(f'percentage gain per level is under the minimal percentage wanted: {level_percentage}', True)
                    
                    raise

                d = {"upperlimit": UPPERLIMIT,
                     "lowerlimit": LOWERLIMIT}

                with open('running_resources\data\grids.json') as f:
                    data = json.load(f)
                data.update(d)

                with open('running_resources\data\grids.json', 'w') as f:
                    json.dump(data, f, indent=4)

                grid_number = 0

                for gridz in range(0, GRIDS+1):

                    gridlevel_down = currentprice-level_price*gridz

                    if gridlevel_down <= LOWERLIMIT:

                        for gridz in range(1, GRIDS+1):

                            gridlevel_up = currentprice+level_price*gridz

                            if gridlevel_up >= UPPERLIMIT:

                                return

                            else:

                                grid_number = grid_number + 1
                                round_gridlevel_up = round(gridlevel_up, 1)
                                d = {f'grid_{grid_number}': {
                                    "price": round_gridlevel_up, "position": "Sell", "order_id": ""}}

                                with open('running_resources\data\grids.json') as f:
                                    data = json.load(f)
                                data.update(d)

                                with open('running_resources\data\grids.json', 'w') as f:
                                    json.dump(data, f, indent=4)

                    else:

                        grid_number = grid_number + 1
                        round_gridlevel_down = round(gridlevel_down, 1)

                        if grid_number == 1:

                            d = {f'grid_{grid_number}': {
                                "price": round_gridlevel_down, "position": "Buy", "order_id": ""}}

                            with open('running_resources\data\grids.json') as f:
                                data = json.load(f)
                            data.update(d)

                            with open('running_resources\data\grids.json', 'w') as f:
                                json.dump(data, f, indent=4)

                        else:

                            d = {f'grid_{grid_number}': {
                                "price": round_gridlevel_down, "position": "Buy", "order_id": ""}}

                            with open('running_resources\data\grids.json') as f:
                                data = json.load(f)
                            data.update(d)

                            with open('running_resources\data\grids.json', 'w') as f:
                                json.dump(data, f, indent=4)

            else:

                print(colored("currentprice is under the lowerlimit", "red"))

                error("currentprice is under the lowerlimit", True)

                raise

        else:

            print(colored("currentprice is above the upperlimit", "red"))
            
            error("currentprice is above the upperlimit", True)

            raise

    else:

        print(colored("upperlimit should be higher than lowerlimit", "red"))

        error("upperlimit should be higher than lowerlimit", True)

        raise
