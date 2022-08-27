from created_session.session import session
from data.config import UPPERLIMIT
from data.config import LOWERLIMIT
from termcolor import colored
import json
from data.error_handle import error
def currentprice():

    all_coins = session.latest_information_for_symbol(
        symbol="BTCUSD"
    )

    if all_coins["ret_msg"] == "OK":

        btc = all_coins["result"][0]
        value_btc = float(btc["last_price"])

        if value_btc > UPPERLIMIT:

            print(colored("price has reached upperlimit cancelling all orders", "red"))
            
            error(f'price has reached upperlimit cancelling all orders', True)

            session.cancel_all_active_orders(
                symbol="BTCUSD"
            )
            position_size = session.my_position(
                symbol="BTCUSD"
            )["result"]["size"]

            if position_size == 0:

                print(colored("position is now 0", "yellow"))
                reset_json()

                raise

            if position_size > 0:

                session.place_active_order(side="Sell", symbol="BTCUSD",
                                       order_type="Market", reduce_only=True, qty=position_size, time_in_force="GoodTillCancel")

                print(colored("position is now 0", "yellow"))
                reset_json()

                raise

            if position_size < 0:

                session.place_active_order(side="Buy", symbol="BTCUSD",
                                       order_type="Market", reduce_only=True, qty=position_size, time_in_force="GoodTillCancel")

                print(colored("position is now 0", "yellow"))
                reset_json()

                raise

        if value_btc < LOWERLIMIT:

            print(colored("price has reached lowerlimit cancelling all orders", "red"))

            error(f'price has reached lowerlimit cancelling all orders', True)

            session.cancel_all_active_orders(
                symbol="BTCUSD"
            )
            position_size = session.my_position(
                symbol="BTCUSD"
            )["result"]["size"]

            if position_size == 0:

                print(colored("position is now 0", "yellow"))
                reset_json()

                raise

            if position_size > 0:

                session.place_active_order(side="Sell", symbol="BTCUSD",
                                              order_type="Market", reduce_only=True, qty=position_size, time_in_force="GoodTillCancel")

                print(colored("position is now 0", "yellow"))
                reset_json()

                raise

            if position_size < 0:

                session.place_active_order(side="Buy", symbol="BTCUSD",
                                              order_type="Market", reduce_only=True, qty=position_size, time_in_force="GoodTillCancel")

                print(colored("position is now 0", "yellow"))
                reset_json()

                raise
        else:

            return value_btc

    else:

        print(
            colored(f'request not aviable error: {all_coins["ret_msg"]}', "red"))

        error(f'request not aviable error: {all_coins["ret_msg"]}', True)

        return
        
def reset_json():
    try:
        with open('grids.json') as f:
            data = json.load(f)

        data = {}

        with open('grids.json', 'w') as f:
            json.dump(data, f, indent=4)

    except FileNotFoundError:

        print(
            colored(f'grids.json could not be found', "red"))
        error('grids.json could not be found', True)

        raise
    
    finally:

        print(colored("grids have been cleared (grids.json)", "green"))