import sqlite3
import numpy as np
import yfinance as yf
import datetime
import threading
from multiprocessing import Process

#Open database for update tickers
update_con = sqlite3.connect(r"/home/recep/CS50/pset8/finance/Tickers.db",check_same_thread=False)
db = update_con.cursor()

# Get tickers list from the database
tickers = list( ticker[0] for ticker in db.execute("SELECT symbol FROM tickers").fetchall())

def update(tickers_update,i):
    print(i)
    #Open database for update1
    update_con = sqlite3.connect(r"/home/recep/CS50/pset8/finance/Tickers.db",check_same_thread=False)
    db = update_con.cursor()

    # Update data
    for ticker in tickers_update:
            
        print(ticker)
        try:
            # Get tickers data from Yahoo Finance
            Ticker = yf.Ticker(ticker).info
            
            try:
                currentPrice = Ticker["currentPrice"]
            except:
                currentPrice = Ticker["ask"]
             
            bid = Ticker["bid"]
            ask =Ticker["ask"]
            change = f"{(currentPrice-Ticker['previousClose'])/Ticker['previousClose']*100:+.2f}%"
            dayLow = Ticker["dayLow"]
            dayHigh = Ticker["dayHigh"]
            volume = Ticker["volume"]
            # Update database for new data
            db.execute("UPDATE tickers SET lastPrice = ?, bid = ?, ask = ?, change = ?, dayLow = ?, dayHigh = ?, volume = ?, date = ? WHERE symbol = ?",
                        [currentPrice, bid, ask, change, dayLow, dayHigh, volume, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ticker])
            update_con.commit()
        except:
            pass
    return True


if __name__=="__main__":

    for i in range(12):
        threading.Thread(target=update, args=(np.array_split(tickers,12)[i],i),).start()
    
    
    
    