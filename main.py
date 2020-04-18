"""Daily Digest uses APIs to fetch things like weather, news, etc. and
format them in a readable format, and email the result to end users"""
#Python 3.x

from newsScrapper import getMajorHeadlines
from weatherScrapper import getCurrentWeather
from sendMail import sendMassIndividualEmails

with open ("endUserEmails.txt", "r") as myfile:
    emails = myfile.read()

USER_EMAILS = eval(emails)

def formatMessage(weatherData, newsData):
    #Extract Weather Data
    tempF = weatherData["TempF"]
    tempC = weatherData["TempC"]
    pressure = weatherData["Pressure"]
    humidity = weatherData["Humidity"]
    weatherDesc = weatherData["Description"]
    windSpeed = weatherData["WindSpeed"]

    #Extract News Data
    articles = newsData

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
    weatherData = getCurrentWeather()
    newsData = getMajorHeadlines()

    messageContent = formatMessage(weatherData, newsData)

    sendMassIndividualEmails(messageContent, USER_EMAILS)

if __name__ == "__main__":
    # execute only if run as a script
    main()
