from simulation import Simulation
from exchange import Exchange
import time

initial_bid_order_depths = {5000: 1}
initial_ask_order_depths = {5001: 1}

ex = Exchange(10000)
sim = Simulation(ex, [0.2, 0.1], 0.3, initial_bid_order_depths, initial_ask_order_depths)

print(ex.get_bid_order_depths(), ex.get_ask_order_depths())

start_time = time.perf_counter()

for i in range(100000):
    sim.step()

end_time = time.perf_counter()

print(ex.get_bid_order_depths(), ex.get_ask_order_depths())
print(end_time - start_time)