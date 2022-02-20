# public-trader
Wrapper class that provides the basic structure for a market making or arbitrage trading bot. This class can be modified for both for market making and for arbitrage, however, you will need to create your own strategies and pricing logic. It is recommended to create child classes that extend the `BaseMarketMaker` class to modify your own strategy.

## Documentation
Detailed documentation can be found within the `base_market_maker.py` file in the form of docstring class documentation and comments.

However, here is a quick summary of what this class handles for you:
* constructur that initializes state variables for tracking orders, prices, etc.
* event loop with logic for sending and refreshing orders
* wrapper functions for the following (these need to be completed by the user in a child class):
  * check_order_fills() -> void
  * delete_all_orders() -> void
  * order_refresh_needed() -> bool
  * process_order_fill() -> void
  * send_limit_order() -> str
  * set_order_levels() -> void
* various other functions that can be extended or overridded

To run the bot, use the `run()` method, which will start the event loop and run the market maker.

It is recommmended to add error handling/logging in your own implementations. API implementations in wrapper classes should ideally be multithreaded and use websocket protocols to prevent slowing down the main loop when receiving data from exchanges, if necessary in your strategy implementation. 
