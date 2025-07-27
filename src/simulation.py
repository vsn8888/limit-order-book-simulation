import numpy as np

class Simulation():
    def __init__(self, exchange, limit_order_arrival_rate, market_order_arrival_rate, initial_bid_order_depths, initial_ask_order_depths):
        self.exchange = exchange
        self.limit_order_arrival_rate = limit_order_arrival_rate
        self.market_order_arrival_rate = market_order_arrival_rate
        self.active_limit_orders = []
        self.active_market_orders = []

        for price in initial_bid_order_depths:
            self.submit_limit_order("BID", price, initial_bid_order_depths[price])
        
        for price in initial_ask_order_depths:
            self.submit_limit_order("ASK", price, initial_ask_order_depths[price])
    
    def step(self):
        new_orders = np.random.binomial(1,
            [[self.market_order_arrival_rate] + self.limit_order_arrival_rate,
             [self.market_order_arrival_rate] + self.limit_order_arrival_rate])

        for i in range(len(new_orders)):
            for j in range(len(new_orders[i])):
                if new_orders[i][j] == 0:
                    continue

                if j == 0:
                    order_type = "BUY" if i == 0 else "SELL"
                    self.submit_market_order(order_type, new_orders[i][j])
                else:
                    order_type = "BID" if i == 0 else "ASK"
                    order_price = self.exchange.get_ask_price() - j if i == 0 else self.exchange.get_bid_price() + j
                    self.submit_limit_order(order_type, order_price, new_orders[i][j])

    def submit_market_order(self, type, quantity):
        for _ in range(quantity):
            self.active_market_orders.append(self.exchange.submit_market_order(type, self))

    def submit_limit_order(self, type, price, quantity):
        for _ in range(quantity):
            self.active_limit_orders.append(self.exchange.submit_limit_order(type, price, self))


