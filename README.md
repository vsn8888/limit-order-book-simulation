# Stochastic Simulation of a Limit Order Book

[Link to notebook](stochastic_simulation.ipynb)

This project involved simulating a stochastic model of a limit order book inspired by [Cont, Stoikov, and Talreja (2010)](http://rama.cont.perso.math.cnrs.fr/pdf/CST2010.pdf). The market order arrivals and limit order arrivals for each price level relative to the opposite best quote are modelled as Poisson processes. A limit order book data structure and order matching algorithm are used to keep track of orders and execute trades.

# Avellaneda-Stoikov Market Making Model

[Link to notebook](avellaneda-stoikov.ipynb)

The Avellaneda-Stoikov market making model ([Avellaneda and Stoikov, 2006](https://people.orie.cornell.edu/sfs33/LimitOrderBook.pdf)) is a market making strategy that deals with the problem of inventory risk. I simulated this market model using the assumption in the literature that the mid price is dictated by a Wiener Process (Brownian Motion). I plan to integrate this strategy with the stochastic simulation of a limit order book described above.



