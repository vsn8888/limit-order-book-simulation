class LimitOrder():
    def __init__(self, type, price, agent):
        self.type = type
        self.agent = agent
        self.price = price
    
    def __lt__(self, other):
        match self.type:
            case "BID":
                if other.type == "BID":
                    return self.price > other.price
                else:
                    return ValueError("Cannot compare limit orders of different types")
            case "ASK":
                if other.type == "ASK":
                    return self.price < other.price
                else:
                    return ValueError("Cannot compare limit orders of different types")
            case _:
                raise ValueError("Limit order type is not valid")