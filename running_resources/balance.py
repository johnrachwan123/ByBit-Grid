from created_session.session import session
from termcolor import colored
import json
from running_resources.data.error_handle import error
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
        error(f'request not aviable error: {wallet["ret_msg"]}', True)
        raise 

def equity_perlevel():

    with open("running_resources\created_session\settings_secret.json", "r") as f:
        data = json.load(f)
    
    GRIDS = data["GRIDS"]
    LOWERLIMIT = data['LOWERLIMIT']
    equity_perlevel = wallet()/GRIDS

    return float(equity_perlevel*LOWERLIMIT)

