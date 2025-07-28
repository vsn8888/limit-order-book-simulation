from simulation import Simulation
from exchange import Exchange
import time
import matplotlib.pyplot as plt
import numpy as np

initial_bid_order_depths = {5000: 15, 4999: 10, 4998: 5}
initial_ask_order_depths = {5001: 15, 5002: 10, 5003: 5}

ex = Exchange(10000)
sim = Simulation(ex, [0.54, 0.29, 0.25, 0.2, 0.1], 1.2, initial_bid_order_depths, initial_ask_order_depths)
length_of_simulation = 5000

print(ex.get_bid_order_depths(), ex.get_ask_order_depths())

start_time = time.perf_counter()

for i in range(length_of_simulation):
    sim.step()
    ex.step(i)
    print(ex.get_bid_order_depths(), ex.get_ask_order_depths())

end_time = time.perf_counter()

print(ex.get_bid_order_depths(), ex.get_ask_order_depths())
print(end_time - start_time)

print(sim.get_orders())

plt.plot(np.arange(length_of_simulation), ex.get_mid_price_history())
plt.show()