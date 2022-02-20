class BaseMarketMaker():    
    '''
    Abstracted Market Maker Base Class that provides the basic structure of order sending/refreshing for a custom market maker. 

    Public Methods:
    - `run()`
    - `dry_run()`

    Methods that shouldn't be overridden:
    - `run()`
    - `refresh_all_orders()`
    - `send_all_orders()`
    
    The following methods must be completed in a child class before running: 
    - `check_order_fills()`
    - `delete_all_orders()`
    - `order_refresh_needed()`
    - `process_order_fill()`
    - `send_limit_order()`
    - `set_order_levels()` 

    The following methods should be inherited with extra code added in as needed:
    - `__init__()` (constructor)

    Other methods are optional, but may be useful when writing the above methods. 

    Note that `clOrdID` is technically different from `orderID`. However, in this implementation they are regarded as the same
    since we save `clOrdID`s as identifying keys in `active_asks` and `active_bids` dictionaries in the `send_all_orders()` method.
    This method can be overridden in child classes to have different uses for clOrdID (client id) and orderID (exchange-returned id).
    '''

    # --- Public methods --- #

    def __init__(self, base: str, quote: str, mm_symbol: str) -> None:        
        """
        Constructor to be inherited by child classes. 

        Args:
            base (str): base asset on market making exchange
            quote (str): quote asset on market making exchange
            mm_symbol (str): symbol on market making exchange

        Initializes the following variables:
        * `self.base` (str)
        * `self.quote` (str)
        * `self.mm_symbol` (str)
        * `self.ask_levels` (dict) planned ask levels to send to market making exchange
        * `self.bid_levels` (dict) planned bid levels to send to market making exchange
        * `self.active_asks` (dict) track active ask order IDs
        * `self.active_bids` (dict) track active bid order IDs 

        Additional variables can be added as required in child classes. 
        """

        # Ticker Info
        self.base = base
        self.quote = quote
        self.mm_symbol = mm_symbol


        # Order Levels Structure:
         
        # Note: order level 0 is the top-of-book quote. If dictionary is empty, it means to not send orders.
        self.ask_levels = {
            # 0: {'clOrdID': 'xxxxxx', 'side': 'sell', 'px': float, 'qty': float, 'alo': bool, ... (other function kwargs as needed) ... params={} (extra request params)},
        }
        self.bid_levels = {
            # 0: {'clOrdID': 'xxxxxx', 'side': 'buy', 'px': float, 'qty': float, 'alo': bool, ... (other function kwargs as needed) ... params={} (extra request params)},
        }

        # Tracking active orders. If the dictionary is empty, it means that there are no orders. 
        self.active_asks = {
            # 0: clOrdID,
            # 1: clOrdID, etc.
        }
        self.active_bids = {
            # 0: clOrdID,
            # 1: clOrdID, etc.
        }

    def run(self):
        '''
        Run the market maker. 
        '''

        # Logic to send orders, refresh orders, etc.

        # In a while loop, use if statements to check and perform action for:
        #   - what to do if an order is filled
        #   - when we need to refresh all orders 
        #   - refresh individual orders

        # Don't forget to check order fills every time after refreshing orders just in case of latency in receiving order fill updates. 
        # If an order is fully/partially filled during a deletion and refresh attempt, we need to process the order fill(s)


        # Boolean Flags
        refresh_individually, refresh_all = False, False

        # Send initial orders to the market making exchange 
        self.send_all_orders()

        # Loop to check for order fills and refresh orders as needed
        while True:
            
            # Check if an immediate order refresh is needed
            refresh_individually, refresh_all = self.order_refresh_needed()

            # If we don't need to immediately refresh orders, then we can check and process any order fills.
            # Note that if we need to refresh orders right away, `self.refresh_orders()` will handle any unexpected order fills. 
            if not refresh_individually and not refresh_all:
                
                # Check for order fills and process fills if necessary
                if self.check_order_fills():
                    self.process_order_fill()
                    
            # Refresh orders if necessary
            if refresh_all:
                self.refresh_all_orders()

                # Boolean Flags
                refresh_individually = False
                refresh_all = False

            elif refresh_individually:
                self.refresh_individual_orders()

                # Boolean Flags
                refresh_individually = False
                refresh_all = False

    def dry_run(self):
        '''
        Performs a dry run of BaseMarketMaker. Prints simulated order levels and config statements without sending real orders. 
        '''        
        pass


    # --- Private Methods --- #

    def check_order_fills(self) -> bool:
        """
        Returns True if any orders were filled, otherwise False. 
        """ 

    def delete_all_orders(self, symbol: str="", verify: bool=True, retries: int = 0) -> bool: 
        """
        Sends a request to delete all active orders on the market making exchange. This action can be made more specific by specifying a symbol.

        Args:
            symbol (str, optional): the symbol for which all orders are deleted. If not set, all active orders are deleted. Defaults to "".
            verify (bool, optional): whether to verify order deletions before terminating the function. Defaults to True.
            retries (int, optional): number of times to resend the request if initial attempt fails. Defaults to 0. 

        Returns:
            bool: by default, returns True if orders were successfully deleted, False if not. However, if `verify` is False then always returns True. 
        """        
        pass

    def delete_order(self, orderID: str, verify: bool=True) -> bool:
        """
        Delete an order on the market making exchange. 

        Args:
            orderID (str): order ID
            verify (bool, optional): whether to verify order deletion before terminating the function. Defaults to True.
        
        Returns:
            bool: by default, returns True if orders were successfully deleted, False if not. However, if `verify` is False then always returns True. 
        """       
        pass

    def order_refresh_needed(self) -> tuple[bool, bool]:
        """
        Checks if we need to refresh orders (either invidually, or all at once) in `self.run()` excluding refreshes after order fills. 
        
        If both `refresh_all` and `refresh_individually` are True, `refresh_all` will take precedence. 
        If you would like to never refresh invidually or never refresh all, set the corresponding value to always return False. 

        Returns:
            tuple[bool, bool]: `tuple[refresh_individually, refresh_all]`. Not mutually exclusive. 
        """
        pass

    def process_order_fill(self):
        """
        What to do after one or more order fills in `self.run()`. 
        
        This function should dynamically handle any order fill and also handle refreshing the required orders. 
        """
        pass

    def query_order_status(self, orderID: str) -> dict:
        """
        Returns the dictionary containing the status of an order on the market making exchange. 

        Args:
            orderID (str): the identifying order ID used to query an order.

        Returns:
            dict: status and information about an order
        """        
    
    def refresh_all_orders(self):
        """
        Refresh all order levels. 

        This function:
        * deletes all orders for the symbol
        * deals with latency order fills
        * sets updated order levels
        * resends orders
        """
        # Algorithm:
        # 1) Retreive updated order levels with `self.set_order_levels()`
        # 2) Bulk Refresh All Orders:
        #    First, bulk delete all orders, and check if any orders were filled during deletion. 
        #    If ANY orders were filled (whether active or deleted), we need to first deal with that before proceeding
        #    Then, send the orders to the market making exchange

        # Delete all orders
        orders_deleted = self.delete_all_orders(self.symbol, verify=True, retries=1)
        if not orders_deleted:
            raise Exception(f'Error Deleting All Orders in {self.refresh_all_orders}.')

        # Check and process any order fills
        if self.check_order_fills():
            self.process_order_fill()

        # Set order levels and resend orders
        self.set_order_levels()
        self.send_all_orders()

    def refresh_individual_orders(self):
        """
        Refresh some set of orders individually.

        This function must handle:
        * retreiving updated order levels (use `self.set_order_levels()`)
        * deleting the required orders 
        * dealing with latency order fills
        * resending the required orders 
        """
        # 1) Retreive updated order levels with `self.set_order_levels()`
        # 2) Refresh Individual Orders:
        #    First, delete the orders that need to be refreshed. 
        #       Note: If ANY orders were filled (whether active or deleted), we need to first deal with that using `self.process_order_fills()` before proceeding
        #    Then, send the orders to the market making exchange
        pass
    
    def send_all_orders(self):
        """
        Send all orders in `self.ask_levels` and `self.bid_levels` to the market making exchange. 
        Run this function only after order levels have already been set by the `self.set_order_levels()` function.
        """

        num_asks = len(self.ask_levels)
        num_bids = len(self.bid_levels)
        iterations = max(num_asks, num_bids)

        for i in range(iterations):
            # Send necessary ask orders
            if i < num_asks:
                kwargs = self.ask_levels[i]
                self.active_asks[i] = self.send_limit_order(**kwargs, verifyOrder=False) # the ** operator unpacks the dictionary and sets key-value pairs as param-arg pairs

            # Send necessary bid orders
            if i < num_bids:
                kwargs = self.bid_levels[i]
                self.active_bids[i] = self.send_limit_order(**kwargs, verifyOrder=False)          

    def send_limit_order(self, clOrdID: str, side: str, px: float, qty: float, symbol: str, 
                            alo: bool, verifyOrder: bool=True, tif: str='GTC', params: dict={}) -> str:              
        """
        Sends a limit order to the market making exchange. 

        Args:
            clOrdID (str): unique client order ID
            side (str): 'buy' or 'sell' order
            px (float): limit order price
            qty (float): order quantity in base asset unit
            symbol (str): trading symbol in 'BASE-QUOTE' format, i.e. 'BTC-USD'
            alo (bool): set `True` to add-liquidity-only (post-only), `False` if it doesn't matter. 
            verifyOrder (bool, optional): Whether to wait for a order confirmation message before terminating the function. Defaults to True.
            tif (str, optional): time-in-force of the order. 'FOK' or 'IOC', or 'GTC'. Defaults to 'GTC'. 
            params (dict, optional): any additional order parameters in the form of a dictionary. Defaults to {}.

        Returns:
            str: returns `clOrdID` once the order is successfully sent to the exchange, or "" if the order fails. If `verifyOrder` is False, returns `clOrdID` immediately after sending the order.
        
        Note: params should be used after manually placing all other parameters in the call. Example:
              binance_api.send_limit_order(clOrdID, side, px, ... tif, **params)
        """            
        pass

    def send_market_order(self, clOrdID: str, side: str, qty: float, symbol: str, verifyOrder: bool=True) -> str:
        """
        Sends a market order to the market making exchange.

        Args:
            clOrdID (str): unique client order ID
            side (str): 'buy' or 'sell' order
            qty (float): order quantity in base asset unit
            symbol (str): trading symbol in 'BASE-QUOTE' format, i.e. 'BTC-USD'
            verifyOrder (bool, optional): Whether or not to wait for a order confirmation message before terminating the function. Defaults to True.

        Returns `clOrdID` if the order is successfully sent to the exchange, otherwise returns an empty string "". 
        However, if `verifyOrder` is set to False then returns `clOrdID` immediately after attempting to send the order. 
        """        
        pass

    def set_order_levels(self):
        '''
        Set planned orders in `self.ask_levels` and `self.bid_levels`.
        '''
        pass

    def verify_order_inactive(self, orderID: str) -> bool:
        """
        Verify if an order is inactive on the market making exchange (whether because it was cancelled or filled). 

        Args:
            orderID (str): the identifying order ID used to query an order.

        Returns:
            bool: True if the order is inactive, False otherwise. 

        NOTE: this function should make use of `self.query_order_status()`
        """     
        pass

    def verify_order_received(self, orderID: str) -> bool:
        """
        Verify if an order was successfully received by the market making exchange. 

        Args:
            orderID (str): the identifying order ID used to query an order.

        Returns:
            bool: True if the order was successfully received, False otherwise.

        NOTE: this function should make use of `self.query_order_status()` 
        """ 
        pass          