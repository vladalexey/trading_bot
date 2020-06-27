from portfolio_manager import PortfolioManager

import alpaca_trade_api as tradeapi
import schedule
import os, json

class PortfolioTrader():

    def __init__(self, 
        funding=4000, 
        barTimeInterval = "minute",
        strategy="sharpe", 
        symbolsList = None):

        BASE_URL = 'https://paper-api.alpaca.markets'

        try:
            with open('./secrets.json') as secrets:
                data = json.load(secrets)

            self.api = tradeapi.REST(
                key_id=data['KeyID'],
                secret_key=data['SecretKey'],
                base_url='https://paper-api.alpaca.markets', api_version='v2'
            )
        except RuntimeError as e:
            raise SystemExit("Not found secrets API key")

        self.strategy = strategy
        self.symbols_list = symbolsList
        self.manager = PortfolioManager(totalFunding=funding, symbolList=symbolsList)

        self.manager.setStockPrices()
        self.manager.optimizePortfolio(strategy)
        self.allocate = self.manager.allocateFunding()[0]

    def monitor(self):

        self.allocate = self.manager.allocateFunding()[0]
        
        for symbol in self.symbols_list:
            self.manager.calculateEMA(symbol)
            order = self.manager.trade_signal(symbol)

            if order and order is True:
                self.place_buy_order(symbol, self.allocate[symbol])
            elif order and order is False:
                self.place_sell_order(symbol, self.allocate[symbol])

    def place_buy_order(self, symbol, num_shares):
        print(symbol, num_shares)

        api.submit_order(
            symbol=symbol,
            qty=num_shares,
            side='buy',
            type='market',
            time_in_force='gtc'
        )

    def place_sell_order(self, symbol, num_shares):
        print(symbol, num_shares)

        api.submit_order(
            symbol=symbol,
            qty=num_shares,
            side='sell',
            type='market',
            time_in_force='gtc'
        )

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
