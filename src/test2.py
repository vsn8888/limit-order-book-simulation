from simulation import Simulation
from exchange import Exchange
import time
import matplotlib.pyplot as plt
import numpy as np

initial_bid_order_depths = {5000: 15, 4999: 10, 4998: 5}
initial_ask_order_depths = {5000: 15, 5002: 10, 5003: 5}

ex = Exchange(10000)
sim = Simulation(ex, [0.54, 0.29, 0.25, 0.2, 0.1], 0.94, initial_bid_order_depths, initial_ask_order_depths)

print(ex.get_ask_order_depths(), ex.get_bid_order_depths())

ex.submit_market_order("BUY", None)
ex.submit_market_order("SELL", None)

ex.step(0)

print(ex.get_ask_order_depths(), ex.get_bid_order_depths())