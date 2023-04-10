from termcolor import colored
import asyncio
from heapq import nsmallest
import json
from .created_session.session import session
# import multiprocessing
from .data.error_handle import error

# Delay can be passed as a variable in the settings.json

delay_tracker =2

async def tracker(currentprice):

    while True:

        await asyncio.sleep(delay_tracker)

        print(colored("tracker is ran", "yellow"))

        if currentprice == False:

            error("current price gives False value", False)

            pass

        with open("running_resources\data\running_resources\data\grids.json", "r") as f:

            data = json.load(f)

        lst = [abs(data[n]['price']-currentprice) for n in data if n != 'upperlimit' and n !='lowerlimit' ]

        three_limiting_case = nsmallest(3, lst)

        try:
            filled_limit = three_limiting_case[0]

        except IndexError:
            print(colored("previous Error occurred [tracker]", "red"))

            error("previous Error occurred [tracker]", True)
        
            raise

        filled_level = lst.index(filled_limit)+1

        print(colored(f'closest grid: {filled_level}', "yellow"))

        if data[f'grid_{filled_level}']["position"] == "Filled":

            limit_one = three_limiting_case[1]
            limit_one_grid = lst.index(limit_one)+1
            limit_two = three_limiting_case[2]
            limit_two_grid = lst.index(limit_two)+1
            print(colored("currentprice is close to filled level", "yellow"))

            if limit_one_grid == limit_two_grid:

                print(
                    colored("upperlimit is equal to lowerlimit", "red"))
                
                error("upperlimit is equal to lowerlimit", True)

                raise

            if data[f'grid_{limit_one_grid}']["price"] > currentprice:

                upperlimit_grid_number = limit_one_grid
                lowerlimit_grid_number = limit_two_grid

            else:

                upperlimit_grid_number = limit_two_grid
                lowerlimit_grid_number = limit_one_grid

            upperlimit_price = data[f'grid_{upperlimit_grid_number}']["price"]
            lowerlimit_price = data[f'grid_{lowerlimit_grid_number}']["price"]

            print(
                colored(f'upperlimit grid number: {upperlimit_grid_number}', 'yellow'))

            print(
                colored(f'lowerlimit grid number: {lowerlimit_grid_number}', "yellow"))

            print(colored("checking limits", "yellow"))

            if data[f'grid_{upperlimit_grid_number}']["position"] == "Sell":

                print(colored("upper limit is satisfied", "green"))

                if data[f'grid_{lowerlimit_grid_number}']["position"] == "Buy":

                    print(colored("lower limit is satisfied", "green"))

                    continue

                else:

                    print(colored("lowerlimit order was not placed yet", "yellow"))

                    order = session.place_active_order(side="Buy", symbol="DOGEUSDT",
                                                          order_type="Limit", price=lowerlimit_price, qty=1, time_in_force="GoodTillCancel")
                    with open('running_resources\data\running_resources\data\grids.json') as f:
                        data = json.load(f)
                    data[f'grid_{lowerlimit_grid_number}']["position"] = "Buy"
                    data[f'grid_{lowerlimit_grid_number}']["order_id"] = order[0]["result"]["order_id"]

                    with open('running_resources\data\grids.json', 'w') as f:
                        json.dump(data, f, indent=4)

                    print(colored("lowerlimit is satisfied", "green"))

                    continue

            else:

                print(colored("upperlimit order was not placed yet", "yellow"))
                order = session.place_active_order(side="Sell", symbol="DOGEUSDT",
                                                      order_type="Limit", price=upperlimit_price, qty=1, time_in_force="GoodTillCancel")

                with open('running_resources\data\grids.json') as f:
                    data = json.load(f)
                data[f'grid_{upperlimit_grid_number}']["position"] = "Sell"
                data[f'grid_{upperlimit_grid_number}']["order_id"] = order[0]["result"]["order_id"]

                with open('running_resources\data\grids.json', 'w') as f:
                    json.dump(data, f, indent=4)

                if data[f'grid_{lowerlimit_grid_number}']["position"] == "Buy":

                    print(colored("upperlimit is satisfied", "green"))

                    continue

                else:

                    print(colored("lowerlimit order was not placed yet", "yellow"))
                    order = session.place_active_order(side="Buy", symbol="DOGEUSDT",
                                                          order_type="Limit", price=lowerlimit_price, qty=1, time_in_force="GoodTillCancel")
                    with open('running_resources\data\grids.json') as f:

                        data = json.load(f)
                    data[f'grid_{lowerlimit_grid_number}']["position"] = "Buy"
                    data[f'grid_{lowerlimit_grid_number}']["order_id"] = order[0]["result"]["order_id"]

                    with open('running_resources\data\grids.json', 'w') as f:
                        json.dump(data, f, indent=4)

                    print(colored("lowerlimit is satisfied", "green"))

                    continue

        else:

            print(colored("price is close to unfilled level, awaiting hit", "yellow"))

            continue


def order_filled_checker(w):
    with open('running_resources\data\grids.json') as f:
        data = json.load(f)
    lst_ordernumbers = [data[n]['order_id'] for n in data if n != 'upperlimit' and n !='lowerlimit']
    ### we get index out of range when there are no grids placed in current price limiting error, want to cancel the order

    try:
        order_id_orderbook_filled = session.get_open_orders(symbol="DOGEUSDT", order_id=lst_ordernumbers[w])["result"]["order_status"]

    except IndexError:

        print(colored("previous Error occurred [order checker]", "red"))

        error("previous Error occurred [order checker]", True)
        
        raise 
   
    try:
        
        if order_id_orderbook_filled == "Filled":

            grid_number_of_filled_order = w+1

            if data[f'grid_{grid_number_of_filled_order}']["position"] == "Filled":

                pass

            else:

                with open('running_resources\data\grids.json') as f:
                    data = json.load(f)

                data[f'grid_{grid_number_of_filled_order}']["position"] = 'Filled'

                with open('running_resources\data\grids.json', 'w') as f:
                    json.dump(data, f, indent=4)

                print(
                    colored(f"New order, data has been processed [{w+1}]", "green"))

                pass

        else:
            pass

    except TypeError:

        print(
            colored("error: Order could not been found completely in filled orders", "red"))

        error("error: Order could not been found completely in filled orders", False)

        pass


def order_filled_checker_processor():

    with open("running_resources\data\settings.json", "r") as f:
        s_data = json.load(f)
    
    GRIDS = s_data["GRIDS"]
    
    global pool_obj
    while True:
        with open('running_resources\data\settings.json') as f:
            data = json.load(f)
        if data["STOP_EXECUTOR"] == "False":
            print(colored("order checker is ran", "yellow"))
            # pool_obj = multiprocessing.Pool(2)
            # pool_obj.map(order_filled_checker, range(0, GRIDS))
            # for i in range(GRIDS):
            #     order_filled_checker(i)
        else:
            try: 
                pool_obj.close()

            except Exception:

                error("error occured during multiprocessing pool [order checker exec]", False)

                pass
            
            finally:
                return