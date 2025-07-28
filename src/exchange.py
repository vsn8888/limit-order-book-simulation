from market_order import MarketOrder
from limit_order import LimitOrder
import heapq
import pandas as pd

class Exchange():
    def __init__(self, ticks):
        self.ticks = ticks
        self.limit_bid_orders = []
        self.limit_ask_orders = []
        self.market_buy_orders = []
        self.market_sell_orders = []
        self.bid_order_depths = {}
        self.ask_order_depths = {}
        self.trades = pd.DataFrame(columns=["time", "buyer", "seller", "price"])
        self.bid_order_depths_history = []
        self.ask_order_depths_history = []
        self.mid_price_history = []
    
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
    
    def get_bid_order_depths_history(self):
        return self.bid_order_depths_history
    
    def get_ask_order_depths_history(self):
        return self.ask_order_depths_history
    
    def get_mid_price_history(self):
        return self.mid_price_history
    
    def get_trades(self):
        return self.trades
    
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
                self.bid_order_depths[limit_order.price] = self.bid_order_depths.get(limit_order.price, 0) + 1
            case "ASK":
                heapq.heappush(self.limit_ask_orders, limit_order)
                self.ask_order_depths[limit_order.price] = self.ask_order_depths.get(limit_order.price, 0) + 1
            case _:
                raise ValueError("Limit order type is invalid")
        
        return limit_order

    def execute_trade(self, buy_order, sell_order, price, time):
        if buy_order.agent:
            buy_order.agent.execute_trade(buy_order, price, time)
        
        if sell_order.agent:
            sell_order.agent.execute_trade(sell_order, price, time)

        self.trades.loc[len(self.trades)] = [time, buy_order.agent, sell_order.agent, price]

    def step(self, time):
        while len(self.limit_ask_orders) != 0 and len(self.market_buy_orders) != 0:
            limit_ask = heapq.heappop(self.limit_ask_orders)
            market_buy = self.market_buy_orders.pop(0)
            if self.ask_order_depths[limit_ask.price] > 1:
                self.ask_order_depths[limit_ask.price] -= 1
            else:
                self.ask_order_depths.pop(limit_ask.price)
            self.execute_trade(market_buy, limit_ask, limit_ask.price, time)

        while len(self.limit_bid_orders) != 0 and len(self.market_sell_orders) != 0:
            limit_bid = heapq.heappop(self.limit_bid_orders)
            market_sell = self.market_sell_orders.pop(0)
            if self.bid_order_depths[limit_bid.price] > 1:
                self.bid_order_depths[limit_bid.price] -= 1
            else:
                self.bid_order_depths.pop(limit_bid.price)
            self.execute_trade(limit_bid, market_sell, limit_bid.price, time)

        while len(self.limit_ask_orders) != 0 and len(self.limit_bid_orders) != 0:
            if self.limit_ask_orders[0].price == self.limit_bid_orders[0].price:
                limit_ask = heapq.heappop(self.limit_ask_orders)
                limit_bid = heapq.heappop(self.limit_bid_orders)

                if self.bid_order_depths[limit_bid.price] > 1:
                    self.bid_order_depths[limit_bid.price] -= 1
                else:
                    self.bid_order_depths.pop(limit_bid.price)

                if self.ask_order_depths[limit_ask.price] > 1:
                    self.ask_order_depths[limit_ask.price] -= 1
                else:
                    self.ask_order_depths.pop(limit_ask.price)

                self.execute_trade(limit_bid, limit_ask, limit_bid.price, time)
            else:
                break
        
        self.bid_order_depths_history.append(self.bid_order_depths)
        self.ask_order_depths_history.append(self.ask_order_depths)
        self.mid_price_history.append((self.get_bid_price() + self.get_ask_price()) / 2)

        # TODO -- Limit order matching against other limit order

