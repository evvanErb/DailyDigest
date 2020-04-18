"""Daily Digest uses APIs to fetch things like weather, news, etc. and
format them in a readable format, and email the result to end users"""
#Python 3.x

from newsScrapper import getMajorHeadlines
from weatherScrapper import getCurrentWeather
from sendMail import sendMassIndividualEmails
from stockScrapper import getMainThreeStocks
import schedule
import time

with open ("endUserEmails.txt", "r") as myfile:
    emails = myfile.read()

USER_DATA = eval(emails)

def formatMessage(weatherData, newsData, stockData):
    #Extract Weather Data
    tempF = weatherData["TempF"]
    tempC = weatherData["TempC"]
    pressure = weatherData["Pressure"]
    humidity = weatherData["Humidity"]
    weatherDesc = weatherData["Description"]
    windSpeed = weatherData["WindSpeed"]

    #Extract News Data
    articles = newsData

    #Extract Stock Data
    stocks = stockData

    #Build Formatted HTMl Message
    #Weather Section
    htmlMessage = ("""
<html>
  <head></head>
  <body>
    <h2>Current Weather</h2>
    <p><b>Temperature: </b>""" + tempF + " / " + tempC
+ "<br><b>Wind Speed: </b>" + windSpeed
+ "<br><b>Pressure: </b>" + pressure
+ "<br><b>Humidity: </b>" + humidity
+ "<br><b>Weather Description: </b>" + weatherDesc)

    #Stock Section
    htmlMessage += "<br><br><h2>Stocks Today\'s Open Yesterday\'s Close</h2>"
    htmlMessage += ("<br>Note if it is the weekend it shows " +
                    "Friday's Open and Close.<br>")
    for stock in stocks:
        htmlMessage += ("<br><b>Symbol: </b>" + stock["Symbol"]
        + "<br><br><b>Today\'s Open Price: </b>$" + stock["OpenPrice"]
        + "<br><b>Yesterday\'s Close Price: </b>$" + stock["LastClosePrice"]
        + "<br>")

    #News Section
    htmlMessage += "<br><br><h2>Top News Stories</h2>"
    #Iterate over all articles and add them to the HTML message
    for article in articles:
        htmlMessage += ("<br><b>Title: </b>" + article["Title"]
        + "<br><br><b>Source: </b>" + article["SourceName"]
        + "<br><b>Date Published: </b>" + article["PublishDate"]
        + "<br><br><b>URL: </b>" + article["Url"]
        + "<br><br><b>Description: </b>" + article["Description"]
        + "<br><br>----------------------<br>")

    #End HTML
    htmlMessage += ("""
    </p>
  </body>
</html>
""")

    return htmlMessage

def main():
    weatherData = getCurrentWeather("19044", "US")
    newsData = getMajorHeadlines()
    stockData = getMainThreeStocks()

    messageContent = formatMessage(weatherData, newsData, stockData)

    sendMassIndividualEmails(messageContent, USER_DATA)

if __name__ == "__main__":
    # execute only if run as a script
    schedule.every().day.at("10:00").do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
