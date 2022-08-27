from tkinter.tix import Tree
from created_session.session import session
from termcolor import colored
from data.config import GRIDS
from data.config import LOWERLIMIT
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

    equity_perlevel = wallet()/GRIDS

    return float(equity_perlevel*LOWERLIMIT)

