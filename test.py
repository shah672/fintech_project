import numpy as np
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
from tabulate import tabulate

sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
stocks = sp500.Symbol.to_list()

start_date = "2017-01-01"
end_date = "2023-01-31"

primary_stocks = []
secondary_stocks = []

for stock in stocks:
    try:
        
        # We should be using adjusted OHLC data as opposed to simply raw data.
        # Adjusted OHLC accounts for corporate actions taken that influence the
        # value of a particular stock such as the payout of dividends, stock splits,
        # rights offerings, and etc.
        
        stock_data = yf.download(stock, start=start_date, end=end_date, auto_adjust=True, repair=True, prepost=False)
        
        # Moving average means that for a given data set, it will examine the first
        # "k" elements before the current row (where applicable; window = k) and
        # perform the specified operation (average in our case).
        
        moving_avg = stock_data["Close"].rolling(window=252).mean()
        
        # The next two lines of code are determining the crossover points in the data
        # when the yearly moving average price is greater than the current close price.
        
        crossover = np.where(stock_data["Close"] > moving_avg, 1, -1)
        crossover = np.sign(np.diff(crossover))
        
        num_positive_crossovers = len(np.where(crossover > 0)[0])
        num_negative_crossovers = len(np.where(crossover < 0)[0])
        
        # Here, a stock is classified as a primary stock if it has a sufficient volume
        # (greater than 1,000,000) and has more positive crossover points than negative.
        
        if stock_data["Volume"].mean() > 1000000:
            if num_positive_crossovers > num_negative_crossovers:
                primary_stocks.append(stock)
            else:
                secondary_stocks.append(stock)
        else:
            secondary_stocks.append(stock)
    except Exception:
        pass
    
def std_dev(stocks, start_date, end_date):
    data = yf.download(stocks, start_date, end_date)['Adj Close']
    ret = data.pct_change()