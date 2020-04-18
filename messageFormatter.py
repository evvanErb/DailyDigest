"""Format HTML Email"""

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
        htmlMessage += "<br><b>Title: </b>" + article["Title"]
        htmlMessage += "<br><br><b>Source: </b>" + article["SourceName"]
        htmlMessage += "<br><b>Date Published: </b>" + article["PublishDate"]
        htmlMessage += "<br><br><b>URL: </b>" + article["Url"]
        try:
            htmlMessage += ("<br><br><b>Description: </b>"
                + article["Description"])
        except:
            print("[!] No Article Description: " + article["Title"])
        htmlMessage += "<br><br>----------------------<br>"

    #End HTML
    htmlMessage += ("""
    </p>
  </body>
</html>
""")

    return htmlMessage
