from multiprocessing import pool
from typing import final
import running_resources.data.config as config
import asyncio
import time
import json
from heapq import nsmallest
from termcolor import colored
import multiprocessing
from pybit.inverse_perpetual import HTTP

session = HTTP("https://api.bybit.com",
               api_key=config.API, api_secret=config.API_SECRET)


def wallet():

    wallet = session.get_wallet_balance(coin="BTC")

    if wallet["ret_msg"] == "OK":
        wallet_btc = wallet["result"]["BTC"]
        print(
            colored(f'avalaible balance: {wallet_btc["available_balance"]}', "yellow"))

        return float(wallet_btc["available_balance"])

    else:

        print(
            colored(f'request not aviable error: {wallet["ret_msg"]}', "red"))
        return


def reset_json():

    with open('grids.json') as f:
        data = json.load(f)

    data = {}

    with open('grids.json', 'w') as f:
        json.dump(data, f, indent=4)

    print(colored("grids have been cleared (grids.json)", "green"))


def currentprice():

    all_coins = session.latest_information_for_symbol(
        symbol="BTCUSD"
    )

    if all_coins["ret_msg"] == "OK":

        btc = all_coins["result"][0]
        value_btc = float(btc["last_price"])

        if value_btc > config.UPPERLIMIT:

            print(colored("price has reached upperlimit cancelling all orders", "red"))

            session.cancel_all_active_orders(
                symbol="BTCUSD"
            )
            position_size = session.my_position(
                symbol="BTCUSD"
            )["result"]["size"]

            if position_size == 0:

                print(colored("position is now 0", "yellow"))
                reset_json()

                return False

            if position_size > 0:

                session.place_active_order(side="Sell", symbol="BTCUSD",
                                       order_type="Market", reduce_only=True, qty=position_size, time_in_force="GoodTillCancel")

                print(colored("position is now 0", "yellow"))
                reset_json()

                return False

            if position_size < 0:

                session.place_active_order(side="Buy", symbol="BTCUSD",
                                       order_type="Market", reduce_only=True, qty=position_size, time_in_force="GoodTillCancel")

                print(colored("position is now 0", "yellow"))
                reset_json()

                return False

        if value_btc < config.LOWERLIMIT:

            print(colored("price has reached lowerlimit cancelling all orders", "red"))

            session.cancel_all_active_orders(
                symbol="BTCUSD"
            )
            position_size = session.my_position(
                symbol="BTCUSD"
            )["result"]["size"]

            if position_size == 0:

                print(colored("position is now 0", "yellow"))
                reset_json()

                return False

            if position_size > 0:

                session.place_active_order(side="Sell", symbol="BTCUSD",
                                              order_type="Market", reduce_only=True, qty=position_size, time_in_force="GoodTillCancel")

                print(colored("position is now 0", "yellow"))
                reset_json()

                return False

            if position_size < 0:

                session.place_active_order(side="Buy", symbol="BTCUSD",
                                              order_type="Market", reduce_only=True, qty=position_size, time_in_force="GoodTillCancel")

                print(colored("position is now 0", "yellow"))
                reset_json()

                return False
        else:

            return value_btc

    else:

        print(
            colored(f'request not aviable error: {all_coins["ret_msg"]}', "red"))

        return


def grid(currentprice):

    print(colored("setting up grid", "yellow"))

    if config.UPPERLIMIT > config.LOWERLIMIT:

        if currentprice < config.UPPERLIMIT:

            if currentprice > config.LOWERLIMIT:

                range_btc = config.UPPERLIMIT - config.LOWERLIMIT
                level_price = range_btc/config.GRIDS
                level_percentage = (level_price/range_btc)*100

                if config.MIN_PERC > level_percentage:
                    print(colored(
                        f'percentage gain per level is under the minimal percentage wanted: {level_percentage}', "red"))
                    return

                d = {"upperlimit": config.UPPERLIMIT,
                     "lowerlimit": config.LOWERLIMIT}

                with open('grids.json') as f:
                    data = json.load(f)
                data.update(d)

                with open('grids.json', 'w') as f:
                    json.dump(data, f, indent=4)

                grid_number = 0

                for gridz in range(0, config.GRIDS+1):

                    gridlevel_down = currentprice-level_price*gridz

                    if gridlevel_down <= config.LOWERLIMIT:

                        for gridz in range(1, config.GRIDS+1):

                            gridlevel_up = currentprice+level_price*gridz

                            if gridlevel_up >= config.UPPERLIMIT:

                                return

                            else:

                                grid_number = grid_number + 1
                                round_gridlevel_up = round(gridlevel_up, 1)
                                d = {f'grid_{grid_number}': {
                                    "price": round_gridlevel_up, "position": "Sell", "order_id": ""}}

                                with open('grids.json') as f:
                                    data = json.load(f)
                                data.update(d)

                                with open('grids.json', 'w') as f:
                                    json.dump(data, f, indent=4)

                    else:

                        grid_number = grid_number + 1
                        round_gridlevel_down = round(gridlevel_down, 1)

                        if grid_number == 1:

                            d = {f'grid_{grid_number}': {
                                "price": round_gridlevel_down, "position": "Buy", "order_id": ""}}

                            with open('grids.json') as f:
                                data = json.load(f)
                            data.update(d)

                            with open('grids.json', 'w') as f:
                                json.dump(data, f, indent=4)

                        else:

                            d = {f'grid_{grid_number}': {
                                "price": round_gridlevel_down, "position": "Buy", "order_id": ""}}

                            with open('grids.json') as f:
                                data = json.load(f)
                            data.update(d)

                            with open('grids.json', 'w') as f:
                                json.dump(data, f, indent=4)

            else:

                print(colored("currentprice is under the lowerlimit", "red"))

        else:

            print(colored("currentprice is above the upperlimit", "red"))

    else:

        print(colored("upperlimit should be higher than lowerlimit", "red"))


def equity_perlevel():

    equity_perlevel = wallet()/config.GRIDS

    return float(equity_perlevel*config.LOWERLIMIT)


def place_orders():

    print(colored("placing all orders at grids", "yellow"))

    with open("grids.json", "r") as f:
        data = json.load(f)

    grid_number = 0

    try:

        for i in range(0, config.GRIDS):

            grid_number = grid_number + 1
            print(grid_number)
            level_price = data[f'grid_{grid_number}']["price"]

            level_position = data[f'grid_{grid_number}']["position"]
            order = session.place_active_order(side=level_position, symbol="BTCUSD",
                                                    order_type="Limit", price=level_price, qty=1, time_in_force="GoodTillCancel")

            with open('grids.json') as f:
                data = json.load(f)
            data[f'grid_{grid_number}']["order_id"] = order["result"]["order_id"]

            with open('grids.json', 'w') as f:
                json.dump(data, f, indent=4)

    except KeyError as e:

        print(colored(
           f'upperlimit or lowerlimit is one of the levels an order want to be placed, change amount of grids or starting value. {e}', "red"))
        with open('settings.json') as f:
            data = json.load(f)
            data["STOP_EXECUTOR"] = "True"
        with open('settings.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        raise 


async def tracker(currentprice):

# changed to async function could be some errors

    while True:

        await asyncio.sleep(2)

        print(colored("tracker is ran", "yellow"))

        if currentprice == False:
            pass

        with open("grids.json", "r") as f:

            data = json.load(f)
        lst = [abs(data[n]['price']-currentprice) for n in data if n != 'upperlimit' and n !='lowerlimit' ]

        three_limiting_case = nsmallest(3, lst)
        try:
            filled_limit = three_limiting_case[0]
        except IndexError:
            print(colored("previous Error occurred [tracker]", "red"))
            with open('settings.json') as f:
                data = json.load(f)
                data["STOP_EXECUTOR"] = "True"
            with open('settings.json', 'w') as f:
                json.dump(data, f, indent=4)
        
            return False
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
                    colored("error: upperlimit is equal to lowerlimit, stopping...", "red"))

                return

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

                    order = session.place_active_order(side="Buy", symbol="BTCUSD",
                                                          order_type="Limit", price=lowerlimit_price, qty=1, time_in_force="GoodTillCancel")
                    with open('grids.json') as f:
                        data = json.load(f)
                    data[f'grid_{lowerlimit_grid_number}']["position"] = "Buy"
                    data[f'grid_{lowerlimit_grid_number}']["order_id"] = order[0]["result"]["order_id"]

                    with open('grids.json', 'w') as f:
                        json.dump(data, f, indent=4)

                    print(colored("lowerlimit is satisfied", "green"))

                    continue

            else:

                print(colored("upperlimit order was not placed yet", "yellow"))
                order = session.place_active_order(side="Sell", symbol="BTCUSD",
                                                      order_type="Limit", price=upperlimit_price, qty=1, time_in_force="GoodTillCancel")

                with open('grids.json') as f:
                    data = json.load(f)
                data[f'grid_{upperlimit_grid_number}']["position"] = "Sell"
                data[f'grid_{upperlimit_grid_number}']["order_id"] = order[0]["result"]["order_id"]

                with open('grids.json', 'w') as f:
                    json.dump(data, f, indent=4)

                if data[f'grid_{lowerlimit_grid_number}']["position"] == "Buy":

                    print(colored("upperlimit is satisfied", "green"))

                    continue

                else:

                    print(colored("lowerlimit order was not placed yet", "yellow"))
                    order = session.place_active_order(side="Buy", symbol="BTCUSD",
                                                          order_type="Limit", price=lowerlimit_price, qty=1, time_in_force="GoodTillCancel")
                    with open('grids.json') as f:

                        data = json.load(f)
                    data[f'grid_{lowerlimit_grid_number}']["position"] = "Buy"
                    data[f'grid_{lowerlimit_grid_number}']["order_id"] = order[0]["result"]["order_id"]

                    with open('grids.json', 'w') as f:
                        json.dump(data, f, indent=4)

                    print(colored("lowerlimit is satisfied", "green"))

                    continue

        else:

            print(colored("price is close to unfilled level, awaiting hit", "yellow"))

            continue


def order_filled_checker(w):
    with open('grids.json') as f:
        data = json.load(f)
    lst_ordernumbers = [data[n]['order_id'] for n in data if n != 'upperlimit' and n !='lowerlimit']
    ### we get index out of range when there are no grids placed in current price limiting error, want to cancel the order
    try:
        order_id_orderbook_filled = session.query_active_order(
                    symbol="BTCUSD",
                order_id=lst_ordernumbers[w]
                    )["result"]["order_status"]
    except IndexError:
        print(colored("previous Error occurred [order checker]", "red"))
        with open('settings.json') as f:
            data = json.load(f)
            data["STOP_EXECUTOR"] = "True"
        with open('settings.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        raise 
   
    try:
        
        if order_id_orderbook_filled == "Filled":

            grid_number_of_filled_order = w+1

            if data[f'grid_{grid_number_of_filled_order}']["position"] == "Filled":

                pass

            else:

                with open('grids.json') as f:
                    data = json.load(f)

                data[f'grid_{grid_number_of_filled_order}']["position"] = 'Filled'

                with open('grids.json', 'w') as f:
                    json.dump(data, f, indent=4)

                print(
                    colored(f"New order, data has been processed [{w+1}]", "green"))

                pass

        else:
            pass

    except TypeError:
        print(
            colored("error: Order could not been found completely in filled orders", "red"))
        raise


def order_filled_checker_processor():
    global pool_obj
    while True:
        with open('settings.json') as f:
            data = json.load(f)
        if data["STOP_EXECUTOR"] == "False":
            print(colored("order checker is ran", "yellow"))
            pool_obj = multiprocessing.Pool(2)
            pool_obj.map(order_filled_checker, range(0, config.GRIDS))
        else:
            try: 
                pool_obj.close()

            except Exception:
                pass
            finally:
                return
