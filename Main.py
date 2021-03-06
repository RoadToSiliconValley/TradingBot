import requests
import argparse

API_URL = "https://www.alphavantage.co/query"

symbols = ['USDCAD']
MagasinValeurRSI = []
MagasinDesPrix = []
tableauDeKeys = ["YGY55JABOFDU3X8Y","BXE971HIQ45YMM8Z","LU8TM1QS01RIUOL2", "OGPYF95QNH7KBH3B","29UFVVR0Q0SJUGRC","WCZ8WZ9NL8YX12X1","JQUOZ93SABS6OVJP"]


def api(symbol):
    temp1 = 0
    temp2 = 0

    data = {"function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": "30min",
            "datatype": "json",
            "apikey": "YGY55JABOFDU3X8Y"}
    response = requests.get(API_URL, data)
    data = response.json()
    a = (data['Time Series (30min)'])

    keys = (a.keys())
    for key in keys:
        MagasinDesPrix.append(a[key]['2. high'])
        temp2 += 1

    data = {"function": "RSI",
             "symbol": symbol,
             "interval": "30min",
             "time_period": "30",
             "series_type": "close",
             "datatype": "json",
             "apikey": "BXE971HIQ45YMM8Z"}
    response = requests.get(API_URL, data)
    data = response.json()
    a = (data['Technical Analysis: RSI'])
    keys = (a.keys())

    for key in keys:
        if temp1 < temp2:
            MagasinValeurRSI.append(a[key]['RSI'])
            temp1 += 1

    return MagasinValeurRSI, MagasinDesPrix


def tradingstrat():
    rsi, prix = api(symbols)
    pipValue= 0
    operation = 0
    initialPrice = 0
    finalPrice = 0
    #if rsi over 70 we sell and buy back when it reaches min value
    file = open("RSI2.txt", 'w', encoding="utf8")
    file.close()
    file = open("RSI2.txt", 'a', encoding="utf8")
    for key in rsi:
        if float(key) > 65:
            currentPrice = prix[rsi.index(key)]
            print("SELL ", currentPrice)
            if operation%2 == 0 :
                initialPrice = currentPrice
                string = "SELLING AT "+ currentPrice+ "\n"
                file.write(string)
                print("initialPrice: ", initialPrice)
                operation += 1
        if float(key) < 52:
            currentPrice = prix[rsi.index(key)]
            print("BUY ", currentPrice)
            if operation%2 == 1:
                finalPrice = currentPrice
                operation+=1
                pipValue = float(initialPrice) - float(finalPrice)
                string = "BUYING AT "+ currentPrice+ "\n"
                file.write(string)
                print("finalPrice: ", initialPrice)

                string= "Profit: "+ str(pipValue) + "\n"
                file.write(string)
                print("PIPVALUE = ", pipValue)
    file.close()

if __name__ == "  main  ":
    parser = argparse.ArgumentParser(prog="main.py")
    parser.add_argument('-a', required=False, help='argument qu on peut ajouter')
    args=parser.parse_args()




tradingstrat()
tableauRSI, prix = api('USDJPY')
print(tableauRSI)
print(prix)










