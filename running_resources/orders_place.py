from created_session.session import session
from termcolor import colored
import json
from data.config import GRIDS
import asyncio
from data.error_handle import error

def place_orders():

    print(colored("placing all orders at grids", "yellow"))
    
    with open("running_resources\created_session\settings_secret.json", "r") as f:
        s_data = json.load(f)
    
    GRIDS = s_data["GRIDS"]

    with open("running_resources\data\grids.json", "r") as f:
        data = json.load(f)


    # use i instead of grid_number could be updated shortly

    grid_number = 0

    try:

        for i in range(0, GRIDS):

            grid_number = grid_number + 1
            print(grid_number)
            level_price = data[f'grid_{grid_number}']["price"]

            level_position = data[f'grid_{grid_number}']["position"]
            order = session.place_active_order(side=level_position, symbol="BTCUSD",
                                                    order_type="Limit", price=level_price, qty=1, time_in_force="GoodTillCancel")

            with open('running_resources\data\grids.json') as f:
                data = json.load(f)
            data[f'grid_{grid_number}']["order_id"] = order["result"]["order_id"]

            with open('running_resources\data\grids.json', 'w') as f:
                json.dump(data, f, indent=4)

    except KeyError as e:

        print(colored(
           f'upperlimit or lowerlimit is one of the levels an order want to be placed, change amount of grids or starting value. {e}', "red"))

        error(f'upperlimit or lowerlimit is one of the levels an order want to be placed, change amount of grids or starting value. {e}', True)
        
        raise 
    
def cancel_all_orders():

    session.cancel_all_active_orders(
                symbol="BTCUSD"
            )

async def place_orders_async():

    print(colored("placing all orders at grids", "yellow"))

    with open("running_resources\data\grids.json", "r") as f:
        data = json.load(f)

    # use i instead of grid_number 

    grid_number = 0

    try:

        for i in range(0, GRIDS):
            grid_number = grid_number + 1
            level_price = data[f'grid_{grid_number}']["price"]

            level_position = data[f'grid_{grid_number}']["position"]
            order = session.place_active_order(side=level_position, symbol="BTCUSD",
                                                    order_type="Limit", price=level_price, qty=1, time_in_force="GoodTillCancel")

            with open('running_resources\data\grids.json') as f:
                data = json.load(f)
            data[f'grid_{grid_number}']["order_id"] = order["result"]["order_id"]

            with open('running_resources\data\grids.json', 'w') as f:
                json.dump(data, f, indent=4)
            await asyncio.sleep(0)

    except KeyError as e:

        print(colored(
           f'upperlimit or lowerlimit is one of the levels an order want to be placed, change amount of grids or starting value. {e}', "red"))

        error(f'upperlimit or lowerlimit is one of the levels an order want to be placed, change amount of grids or starting value. {e}', True)
        
        raise 