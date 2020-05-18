from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

import pandas as pd
from pandas_datareader import data as web
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
 
class PortfolioManager():

    def __init__(self, 
            totalFunding=300, 
            start_date='2013-01-01', 
            symbolList=["FB", "AMZN", "AAPL", "NFLX", "GOOG"]):
        
        super().__init__()
        self.totalFunding = totalFunding
        self.assets = symbolList
        #Create a dataframe to store the adjusted close price of the stocks
        self.df = pd.DataFrame()
        #Get the stock starting date
        self.stockStartDate = start_date
        self.cleaned_weights = None

    def setStockPrices(self):
        # Get the stocks ending date aka todays date and format it in the form YYYY-MM-DD
        today = datetime.today().strftime('%Y-%m-%d')

        #Store the adjusted close price of stock into the data frame
        for stock in assets:
            self.df[stock] = web.DataReader(
                stock,
                data_source='yahoo',
                start=stockStartDate , 
                end=today)['Adj Close']

    def plotStockPrices(self):
        # Create the title 'Portfolio Adj Close Price History
        title = 'Portfolio Adj. Close Price History'
        #Get the stocks
        my_stocks = self.df
        #Create and plot the graph
        plt.figure(figsize=(12.2,4.5)) #width = 12.2in, height = 4.5
        
        # Loop through each stock and plot the Adj Close for each day
        for c in my_stocks.columns.values:
            plt.plot( my_stocks[c],  label=c)#plt.plot( X-Axis , Y-Axis, line_width, alpha_for_blending,  label)
        
        plt.title(title)
        plt.xlabel('Date',fontsize=18)
        plt.ylabel('Adj. Price USD ($)',fontsize=18)
        plt.legend(my_stocks.columns.values, loc='upper left')

        plt.show()

    def calculateMu(self):
        mu = expected_returns.mean_historical_return(df)#returns.mean() * 252
        return mu

    def calculateSampleCovarianceMatrix(self):
        S = risk_models.sample_cov(df) #Get the sample covariance matrix
        return S

    def optimizePortfolio(self):
        '''
            Optimize for maximal Sharpe ratio
            TODO: Allow for more options
            Return EfficientFrontier object
        '''

        mu = self.calculateMu()
        S = self.calculateSampleCovarianceMatrix()
        ef = EfficientFrontier(mu, S)

        weights = ef.max_sharpe() #Maximize the Sharpe ratio, and get the raw weights
        self.cleaned_weights = ef.clean_weights() 
        print(self.cleaned_weights) #Note the weights may have some rounding error, meaning they may not add up exactly to 1 but should be close
        ef.portfolio_performance(verbose=True)

        return ef

    def allocateFunding(self):
        '''
            Allocate available funding to stock in assets
            Return 
                allocation [rtype: dict]
                leftover [rtype: float]
        '''

        latest_prices = get_latest_prices(self.df)
        da = DiscreteAllocation(
            self.weights, 
            latest_prices, 
            total_portfolio_value=self.totalFunding)

        allocation, leftover = da.lp_portfolio()
        print("Discrete allocation:", allocation)
        print("Funds remaining: ${:.2f}".format(leftover))

        return allocation, leftover