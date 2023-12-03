import sqlite3
import csv
import yfinance as yf

def main():
    con = sqlite3.connect("/home/recep/CS50/Finance_db/Tickers.db")
    db = con.cursor()

    with open("/home/recep/CS50/Finance_csv/Companies+.csv",newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        for row in reader:
            try:
                db.execute("INSERT INTO tickers(symbol, name) VALUES (?, ?)",[row[0], yf.Ticker(row[0]).info["longName"]])
            except:
                db.execute("INSERT INTO tickers(symbol, name) VALUES (?, ?)",[row[0], input(row[0])])
            con.commit()


if __name__=="__main__":
    main()