from market_order import MarketOrder
from limit_order import LimitOrder
import heapq

class Exchange():
    def __init__(self, ticks):
        self.ticks = ticks
        self.limit_bid_orders = []
        self.limit_ask_orders = []
        self.market_buy_orders = []
        self.market_sell_orders = []
        self.bid_order_depths = {}
        self.ask_order_depths = {}
    
    def get_bid_price(self):
        if len(self.limit_bid_orders) == 0:
            return 0
        else:
            return self.limit_bid_orders[0].price

    def get_ask_price(self):
        if len(self.limit_ask_orders) == 0:
            return self.ticks + 1
        else:
            return self.limit_ask_orders[0].price
        
    def get_bid_order_depths(self):
        return self.bid_order_depths
    
    def get_ask_order_depths(self):
        return self.ask_order_depths
    
    def submit_market_order(self, type, agent):
        market_order = MarketOrder(type, agent)
        
        match type:
            case "BUY":
                self.market_buy_orders.append(market_order)
            case "SELL":
                self.market_sell_orders.append(market_order)
            case _:
                raise ValueError("Market order type is invalid")
        
        return market_order

    def submit_limit_order(self, type, price, agent):
        limit_order = LimitOrder(type, max(1, min(price, self.ticks)), agent)
        
        match type:
            case "BID":
                heapq.heappush(self.limit_bid_orders, limit_order)
                self.bid_order_depths[price] = self.bid_order_depths.get(price, 0) + 1
            case "ASK":
                heapq.heappush(self.limit_ask_orders, limit_order)
                self.ask_order_depths[price] = self.ask_order_depths.get(price, 0) + 1
            case _:
                raise ValueError("Limit order type is invalid")
        
        return limit_order
