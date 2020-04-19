"""Daily Digest uses APIs to fetch things like weather, news, etc. and
format them in a readable format, and email the result to end users"""
#Python 3.x

from newsScrapper import getMajorHeadlines
from weatherScrapper import getWeather
from sendMail import sendMassIndividualEmails
from stockScrapper import getMainThreeStocks
from messageFormatter import formatMessage
import schedule
import time

with open ("endUserEmails.txt", "r") as myfile:
    emails = myfile.read()

USER_DATA = eval(emails)

def main():
    weatherData = getWeather("19044", "US")
    newsData = getMajorHeadlines()
    stockData = getMainThreeStocks()

    messageContent = formatMessage(weatherData, newsData, stockData)

    sendMassIndividualEmails(messageContent, USER_DATA)

if __name__ == "__main__":
    # execute only if run as a script
    schedule.every().day.at("10:00").do(main)
    while True:
        schedule.run_pending()
        time.sleep(30)
