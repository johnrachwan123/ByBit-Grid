import asyncio
from termcolor import colored
from concurrent.futures import ProcessPoolExecutor
from old_stuff.bot import order_filled_checker_processor, tracker
from old_stuff.bot import currentprice
from old_stuff.bot import place_orders
from old_stuff.bot import grid
from old_stuff.bot import order_filled_checker_processor
import config

if __name__ == "__main__":

    if config.RUN_ONLY_ORDERCHECKS == True:

        print(colored("starting ByBit client", "yellow"))

        print(colored("successful started ByBit client", "green"))

        executor = ProcessPoolExecutor()
        loop = asyncio.get_event_loop()
        loop.run_in_executor(executor, order_filled_checker_processor)
        loop.run_until_complete(tracker(currentprice=currentprice()))
        loop.run_forever()

    else:

        print(colored("starting ByBit client", "yellow"))

        print(colored("successful started ByBit client", "green"))
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
