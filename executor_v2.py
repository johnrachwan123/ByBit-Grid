import asyncio
from termcolor import colored
from concurrent.futures import ProcessPoolExecutor
from running_resources.setup_grids import grid
from running_resources.currentprice import currentprice
from running_resources.synch_check import order_filled_checker_processor
from running_resources.synch_check import tracker
from running_resources.orders_place import place_orders
import json

# for later usage we could run a module in the error script that is called initial error check, that checks if all json files are json files, all settings are filled in etc.

if __name__ == "__main__":

    with open("running_resources\data\settings.json", "r") as f:
        s_data = json.load(f)
    
    RUN_ONLY_ORDERCHECKS = s_data["RUN_ONLY_ORDERCHECKS"]

    if RUN_ONLY_ORDERCHECKS == True:

        print(colored("starting ByBit client", "yellow"))

        #print(colored("successful started ByBit client", "green"))

        executor = ProcessPoolExecutor()
        loop = asyncio.get_event_loop()
        loop.run_in_executor(executor, order_filled_checker_processor)
        loop.run_until_complete(tracker(currentprice=currentprice()))
        loop.run_forever()

    else:

        print(colored("starting ByBit client", "yellow"))

        #print(colored("successful started ByBit client", "green"))
        grid(currentprice=currentprice())

        print(colored("setting up grid succesfull", "green"))

        place_orders()

        print(colored("all orders have succesfully been placed", "green"))
        executor = ProcessPoolExecutor(1)
        loop = asyncio.get_event_loop()
        loop.run_in_executor(executor, order_filled_checker_processor)
        loop.run_in_executor(executor, tracker(currentprice=currentprice()))
        #loop.run_until_complete(tracker(currentprice=currentprice()))
        try:
            loop.run_forever()
        except Exception as e:
            print(f"Error occured in loop asyncio. {e}")
