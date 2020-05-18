from portfolio_manager import PortfolioManager

import alpaca_trade_api as tradeapi
from datetime import datetime
import matplotlib.pyplot as plt

class PortfolioTrader():

    def __init__(self, funding = 500, barTimeInterval = "minute", symbolsList = None):
        self.api = tradeapi.REST()
        self.symbols_list = symbolsList
        self.manager = PortfolioManager(totalFunding=funding, symbolList=symbolsList)

    def place_buy_order(self):
        pass

    def place_sell_order(self):
        pass

    def system_loop(self):
        pass