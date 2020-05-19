from portfolio_manager import PortfolioManager

import alpaca_trade_api as tradeapi
import os, json

class PortfolioTrader():

    def __init__(self, 
        funding=4000, 
        barTimeInterval = "minute",
        strategy="sharpe", 
        symbolsList = None):

        try:
            with open('./secrets.json') as secrets:
                data = json.load(secrets)

            self.api = tradeapi.REST(
                key_id=data['KeyID'],
                secret_key=data['SecretKey']
            )
        except RuntimeError as e:
            raise SystemExit("Not found secrets API key")
        
        self.strategy = strategy
        self.symbols_list = symbolsList
        self.manager = PortfolioManager(totalFunding=funding, symbolList=symbolsList)

        self.manager.setStockPrices()
        self.manager.optimizePortfolio(strategy)
        self.manager.allocateFunding()

    def place_buy_order(self):
        pass

    def place_sell_order(self):
        pass

    def system_loop(self):
        pass


if __name__ == "__main__":
    trader = PortfolioTrader(
        funding=4000,
        strategy='volatility',
        symbolsList=[
            "MDB",
            "PYPL",
            "DDOG",
            "NVDA",
            "V",
            "MA",
            "TEAM",
            "FB", 
            "AMZN", 
            "AAPL", 
            "NFLX", 
            "GOOG",
        ])    

    