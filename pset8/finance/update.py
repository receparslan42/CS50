from datetime import datetime
import threading
import sqlite3
import yfinance as yf
import numpy as np

# Open database for show tickers
Tickers_con = sqlite3.connect(r"/home/recep/CS50/pset8/finance/Tickers.db", check_same_thread=False)
Tickers_cur = Tickers_con.cursor()

Data=[]
def update(Tickers):
    
    for ticker in Tickers:
        
        try:
            # Get tickers data from Yahoo Finance
            Ticker = yf.Ticker(ticker).info
        except:
            Check = True
            while Check:
                try:
                    # Get tickers data from Yahoo Finance
                    Ticker = yf.Ticker(ticker).info
                    Check = False
                except:
                    Check=True
        try:
            currentPrice = Ticker["currentPrice"]
        except:
            currentPrice = Ticker["ask"]
        try:
            bid = Ticker["bid"]
            ask = Ticker["ask"]
        except:
            bid = Ticker["currentPrice"]
            ask = Ticker["currentPrice"]
        change = f"{(currentPrice-Ticker['previousClose'])/Ticker['previousClose']*100:+.2f}%"
        dayLow = Ticker["dayLow"]
        dayHigh = Ticker["dayHigh"]
        volume = Ticker["volume"]
        
        tickers = [currentPrice, bid, ask, change, dayLow, dayHigh, volume, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ticker]
        Data.append(tickers)

def get_data():
    
    # Get tickers list from the database
    Tickers = list( ticker[0] for ticker in Tickers_cur.execute("SELECT symbol FROM tickers").fetchall())
    tickers = np.array_split(Tickers,25)

    # Start threads
    Threads = []
    for i in range(25):
        Thread =threading.Thread(target=update, args=(tickers[i],))
        Thread.start()
        Threads.append(Thread)
    
    for thread in Threads:
        thread.join()
    
    #Update database for tickers
    for ticker in Data:
        # Update database for new data
        Tickers_cur.execute("UPDATE tickers SET lastPrice = ?, bid = ?, ask = ?, change = ?, dayLow = ?, dayHigh = ?, volume = ?, date = ? WHERE symbol = ?",ticker)
        Tickers_con.commit()
            
    return get_data()
