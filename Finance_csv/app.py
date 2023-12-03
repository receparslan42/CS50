import csv
import yfinance as yf
def main():

    #Open Companies file
    with open('/home/recep/CS50/Finance/Companies.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')


        for row in reader:
            try:
                if yf.Ticker(row[0]+".IS").info:
                    #Open Companies+ file for add companies which have bist
                    with open('/home/recep/CS50/Finance/Companies+.csv', 'a',newline='') as csvfile2:
                        writer = csv.writer(csvfile2, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        writer.writerow([row[0]+".IS"])
            except:
                #Open Companies- file for add companies which have not bist
                with open('/home/recep/CS50/Finance/Companies-.csv', 'a',newline='') as csvfile2:
                    writer = csv.writer(csvfile2, delimiter=' ', quotechar= '|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([row[0]])



if __name__ == "__main__":
    main()