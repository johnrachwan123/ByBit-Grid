from .created_session.session import session
from termcolor import colored
import json
from .data.error_handle import error

def extract_current_price(order_book_snapshot):
    top_bid_price = float(order_book_snapshot['result']['b'][0][0])
    top_ask_price = float(order_book_snapshot['result']['a'][0][0])
    current_price = (top_bid_price + top_ask_price) / 2
    return current_price

def currentprice():
    with open("running_resources\data\settings.json", "r") as f:
        data = json.load(f)
    
    UPPERLIMIT = data["UPPERLIMIT"]
    LOWERLIMIT = data['LOWERLIMIT']
    
    all_coins = session.get_orderbook(category='linear',
        symbol="DOGEUSDT"
    )
    if all_coins["retMsg"] == "OK":

        # btc = all_coins["result"][0]
        # value_btc = float(btc["last_price"])
        value_btc = extract_current_price(all_coins)
        if value_btc > UPPERLIMIT:

            print(colored("price has reached upperlimit cancelling all orders", "red"))
            
            error(f'price has reached upperlimit cancelling all orders', True)

            session.cancel_all_active_orders(
                symbol="DOGEUSDT"
            )
            position_size = session.my_position(
                symbol="DOGEUSDT"
            )["result"]["size"]

            if position_size == 0:

                print(colored("position is now 0", "yellow"))
                reset_json()

                raise

            if position_size > 0:

                session.place_order(category='limit', side="Sell", symbol="DOGEUSDT",
                                       order_type="Market", reduce_only=True, qty=position_size)

                print(colored("position is now 0", "yellow"))
                reset_json()

                raise

            if position_size < 0:

                session.place_order(category='linear', side="Buy", symbol="DOGEUSDT",
                                       order_type="Market", reduce_only=True, qty=position_size)

                print(colored("position is now 0", "yellow"))
                reset_json()

                raise

        if value_btc < LOWERLIMIT:

            print(colored("price has reached lowerlimit cancelling all orders", "red"))

            error(f'price has reached lowerlimit cancelling all orders', True)

            session.cancel_all_active_orders(
                symbol="DOGEUSDT"
            )
            position_size = session.my_position(
                symbol="DOGEUSDT"
            )["result"]["size"]

            if position_size == 0:

                print(colored("position is now 0", "yellow"))
                reset_json()

                raise

            if position_size > 0:

                session.place_order(category='limit', side="Sell", symbol="DOGEUSDT",
                                              order_type="Market", reduce_only=True, qty=position_size)

                print(colored("position is now 0", "yellow"))
                reset_json()

                raise

            if position_size < 0:

                session.place_order(category='limit', side="Buy", symbol="DOGEUSDT",
                                              order_type="Market", reduce_only=True, qty=position_size)

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