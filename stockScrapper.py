"""This file contains functions to scrap news websites and format the
results for easy reading"""
#Python 3.x

import requests, json, datetime

with open ("passwords.txt", "r") as myfile:
    keysAndPasses = myfile.read()

keysAndPasses = eval(keysAndPasses)
STOCK_API_KEY = keysAndPasses["STOCK_API_KEY"]
BASE_URL = "https://www.alphavantage.co/query?"


#Gets the data for a stocks open price today and close price yesterday
#(Or the nearest weekdays) and returns them
def getStockOCData(symbol):
    timeFunction = "TIME_SERIES_DAILY"
    interval = "60min"
    outputsize = "compact"

    completeUrl = (BASE_URL + "function=" + timeFunction +
                    "&symbol=" + symbol + "&interval=" + interval +
                    "&outputsize=" + outputsize + "&apikey=" + STOCK_API_KEY)

    #Get data and extract in JSON format
    response = requests.get(completeUrl)
    jsonData = response.json()

    formattedResponse = {}

    try:
        #Get todays date
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        dayOfWeek = today.weekday()

        #If its a week adjust to last weekday to get stock data
        if dayOfWeek == 6:
            today = today - datetime.timedelta(days=2)
            yesterday = today - datetime.timedelta(days=2)

        elif dayOfWeek == 5:
            today = today - datetime.timedelta(days=1)

        elif dayOfWeek == 0:
            yesterday = today - datetime.timedelta(days=3)

        #Formate date
        todaysDate = today.strftime("%Y-%m-%d")
        yesterdaysDate = yesterday.strftime("%Y-%m-%d")

        #Get daily data and todays data
        timeSeries  = jsonData["Time Series (Daily)"]
        todaysData = timeSeries[todaysDate]
        yesterdaysData = timeSeries[yesterdaysDate]

        #Extract todays data and add to formattedResponse
        openPrice = todaysData["1. open"]
        lastClose = yesterdaysData["4. close"]

        formattedResponse["Symbol"] = symbol
        formattedResponse["OpenPrice"] = str(round(float(openPrice), 2))
        formattedResponse["LastClosePrice"] = str(round(float(lastClose), 2))

        return formattedResponse

    except:
        raise Exception ("[!] Error #1: Could not access stock data: "
                + symbol + " : " + jsonData)


#Gets Open today / Close yest prices of the 3 main
#stock indexes and returns them
def getMainThreeStocks():
    formattedResponse = []

    #Iterate over the 3 major stock indexes and get their data and add them to
    #the response
    for symbol in ["QQQ", "INX", "DJI"]:
        formattedResponse.append(getStockOCData(symbol))

    return formattedResponse
