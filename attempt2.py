import numpy as np
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
from tabulate import tabulate
import matplotlib.pyplot as plt

sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
stocks = sp500.Symbol.to_list()

primary_stocks = []
secondary_stocks = []

start_date = "2022-12-12"
end_date = "2023-06-09"

def calculate_rsi(stock_data):
#    stock_data = yf.download(stock_name, start=start_date, end=end_date, repair=True, prepost=False)
    
    daily_change = stock_data["Close"].diff()
    daily_change.dropna(inplace=True)
    
    positive_change = daily_change.copy()
    positive_change[positive_change < 0] = 0
    
    negative_change = daily_change.copy()
    negative_change[negative_change > 0] = 0
    
    average_change_positive = positive_change.rolling(14).mean()
    average_change_negative = negative_change.rolling(14).mean().abs()
    
    rsi = 100 * average_change_positive / (average_change_positive + average_change_negative)
    rsi = pd.DataFrame(rsi)
    rsi.columns = ["RSI"]
    
    return rsi

def calculate_stocastic_oscillator(stock_data):
#    stock_data = yf.download(stock_name, start=start_date, end=end_date, repair=True, prepost=False)
    
    high = stock_data["High"].rolling(14).max()
    low = stock_data["Low"].rolling(14).min()
    
    stock_data["FSO"] = 100 * (stock_data["Close"] - low) / (high - low)
    stock_data["SSO"] = stock_data["FSO"].rolling(3).mean()
    stock_data["FSO-SSO"] = stock_data["FSO"] - stock_data["SSO"]
    
    
    return stock_data[["FSO","SSO", "FSO-SSO"]]

# It is an indication to buy when the MACD line is above the 9-day EMA of MACD.

def calculate_macd(stock_data):
#    stock_data = yf.download(stock_name, start=start_date, end=end_date, repair=True, prepost=False)
    
    ema12 = stock_data["Close"].ewm(span=12).mean()
    ema26 = stock_data["Close"].ewm(span=26).mean()
    
    macd = ema12 - ema26
    macd = pd.DataFrame(macd)
    signal_line = macd.ewm(span=9).mean()
        
    difference = macd - signal_line
    difference = pd.DataFrame(difference)
    
    macd.columns = ["MACD"]
    macd["Signal Line"] = signal_line
    macd["Difference"] = macd["MACD"] - macd["Signal Line"]
    
    difference.columns = ["MACD"]
    
    return macd

# An ADX value below 20 indicates weak trend, whereas a value above 40 indicates a strong trend.
# When the +DI value crosses above the -DI value, this is considered a bullish situation.
# Conversely, when the -DI value crosses above the +DI value, this is considered bearish.

def calculate_dmi(stock_data):
#    stock_data = yf.download(stock_name, start=start_date, end=end_date, repair=True, prepost=False)
    
    stock_data["+DM"] = stock_data["High"].diff()
    stock_data["-DM"] = stock_data["Low"].diff()
    
    stock_data.loc[stock_data["+DM"] < 0, "+DM"] = 0
    stock_data.loc[stock_data["-DM"] > 0, "-DM"] = 0
    
    stock_data["TR1"] = stock_data["High"] - stock_data["Low"]
    stock_data["TR2"] = abs(stock_data["High"] - stock_data["Close"].shift(1))
    stock_data["TR3"] = abs(stock_data["Low"] - stock_data["Close"].shift(1))

    stock_data["Max"] = stock_data[["TR1", "TR2", "TR3"]].max(axis=1)
    
    stock_data["ATR"] = stock_data["Max"].rolling(window=14).mean()

    stock_data["+DI"] = 100 * (stock_data["+DM"].ewm(alpha= 1/14).mean() / stock_data["ATR"])
    stock_data["-DI"] = abs(100 * (stock_data["-DM"].ewm(alpha= 1/14).mean() / stock_data["ATR"]))

    dx = 100 * (abs(stock_data["+DI"] - stock_data["-DI"]) / abs(stock_data["+DI"] + stock_data["-DI"]))
    adx = ((dx.shift(1) * 13) + dx) / 14
    stock_data["ADX"] = adx.ewm(alpha=1/14).mean()
    
    stock_data["+DI/-DI"] = stock_data["+DI"] - stock_data["-DI"]
    
    return stock_data

def plot_indicators(stock):
    stock_data = yf.download(stock, start=start_date, end=end_date, repair=True, prepost=False)
    
    rsi = calculate_rsi(stock_data)
    stocastic_oscillator  = calculate_stocastic_oscillator(stock_data)
    macd = calculate_macd(stock_data)
    dmi = calculate_dmi(stock_data)
    
    rsi.reset_index(inplace=True)
    stocastic_oscillator.reset_index(inplace=True)
    macd.reset_index(inplace=True)
    dmi.reset_index(inplace=True)
    
    r = rsi.plot(x='Date', y='RSI', kind='line')
    r.axhline(y=70, color='red')
    r.axhline(y=30, color='green')
    so = stocastic_oscillator.plot(x='Date', y='FSO', kind='line')
    stocastic_oscillator.plot(ax=so, x='Date', y='SSO')
    os = dmi.plot(x='Date', y='+DI', kind='line')
    dmi.plot(ax=os, x='Date', y='-DI')
    m = macd.plot(x='Date', y='MACD', kind='line')
    macd.plot(ax=m, x='Date', y='Signal Line')
    
    plt.show()

def create_portfolio(stock):
    
    rsi_indicator = False
    stocastic_oscillator_indicator = False
    dmi_indicator = False
    macd_indicator = False
    
    #for stock in stocks:
    try:
        stock_data = yf.download(stock, start=start_date, end=end_date, repair=True, prepost=False)
    
        rsi = calculate_rsi(stock_data)
        print('RSI', rsi.iloc[-1]["RSI"])
        if rsi.iloc[-1]["RSI"] < 50:
            rsi_indicator = True
        else:
            rsi_indicator = False
        stocastic_oscillator = calculate_stocastic_oscillator(stock_data)
        print("SO", stocastic_oscillator.iloc[-1]["FSO-SSO"])
        if stocastic_oscillator.iloc[-1]["FSO-SSO"] > 0:
            stocastic_oscillator_indicator = True
        else:
            stocastic_oscillator_indicator = False
        
        macd = calculate_macd(stock_data)
        print("MACD", macd.iloc[-1]["MACD"])        
        if macd.iloc[-1]["MACD"] > 0:
            macd_indicator = True
        else:
            macd_indicator = False
            
        dmi = calculate_dmi(stock_data)
        print("DMI", dmi.iloc[-1]["+DI/-DI"])
        if dmi.iloc[-1]["+DI/-DI"] > 0:
            dmi_indicator = True
        else:
            dmi_indicator = False
            
        if rsi_indicator and dmi_indicator and macd_indicator and stocastic_oscillator_indicator:
            primary_stocks.append(stock)
    except Exception:
        pass
#    print(primary_stocks)
    return primary_stocks
        
# for stock in stocks:
#     print(stock, create_portfolio(stock))
plot_indicators("AMZN")