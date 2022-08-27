# ByBit

## SETUP:
Fill in bybit API-, API SECRET-KEY into the session secret_settings.json
Alternating from the strategy you would like to follow it can be done by changing the settings.json with the limits you would like.

## GUIDE/STRATEGY:
When setting the bot right up, the bot wil place orders accordingly to the price ranges that have been given and the amount of grids chosen.
These will be placed inside the Bybit trading platfrom. Above the intial price short/sell orders will be place and below the initial price long/buy orders will be placed.
Accordingly if the price of your chosen coin [only bitcoin supported] goes up from the initial price and hits a (in this case) short/sell order the initial grid,
it was on will now become a buy order. This happends also visa versa when the price goes down and the above gride becomes a short/sell order. 
This will take place until the price has reached the upperlimit or lowerlimit of your chosen setting.

## RECOMMENDATION:
For this type of bot a lot of assets are needed because you want to maximize the amount of grids your can use. As of now we do not have a standard limit inside the bot.
The only limiting case is the amount of limit orders that can be place by Bybit. [We could maximize this by using double API keys, but as of now that needs extra reaserch.]

## ALSO INCLUDED:
Very low cpu usage bot therefore it does not need any resources and can even be ran on a simple raspberry pi [couple of users only]. Error logging has been accomoplished,
in the sense that in error.json the timestamp and error code will be sourced. Therefore when hitting a error in the system it can easily be found and replaced or asked to the creator(s).
Beside all the data can be tracked in the log of the running bot where it will state what it is running. (Most of the time it is the checking and tracking part of the orders.)
All the grid data can be found in grids.json including the status, price, position and grid number. 

## COMING UP:
A website in development for tracking your assets and your orders. Including your settings with API-keys. If that is a succes we look into creatnig and application
used on the phone.


This website and its content is copyright of Currency Finn - © Currency Finn 2022-2023. All rights reserved.
