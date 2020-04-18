"""This file contains functions to scrap weather websites and format the
results for easy reading"""
#Python 3.x

import requests, json, re
from bs4 import BeautifulSoup

with open ("passwords.txt", "r") as myfile:
    keysAndPasses = myfile.read()

keysAndPasses = eval(keysAndPasses)

with open ("settings.txt", "r") as myfile:
    settings = myfile.read()

settings = eval(settings)

WEATHER_SCRAPE = settings["WEATHER_SCRAPE"]
OPEN_WEATHER_API_KEY = keysAndPasses["OPEN_WEATHER_API_KEY"]
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/"
WEATHER_SCRAPE_URL = "https://weather.com/weather/today/l/"

#Screapes weather.com for todays weather at zipcode
def getTodaysWeatherScrape(zipCode, countryCode):
    completeUrl = WEATHER_SCRAPE_URL + zipCode

    #Get HTML data and setup soup
    page = requests.get(completeUrl)
    soup = BeautifulSoup(page.content, "html.parser")

    #Find proper HTML sections
    tempElems = soup.find("div", class_="today_nowcard-temp")
    phraseElems = soup.find("div", class_="today_nowcard-phrase")
    panelElems = soup.find("div", class_="today_nowcard-sidecar component panel")

    #Extract text from found HTML
    tempExtracted = tempElems.text
    phraseExtracted = phraseElems.text
    panelExtracted = panelElems.text

    tempF = tempExtracted + " F"

    #Convert F to C
    rawTempC = round(((float(tempExtracted[:-1]) - 32) * (5/9)), 1)
    tempC = str(rawTempC) + tempExtracted[-1] + " C"

    #Extract proper data from panel via regex
    humidity = (re.findall("[0-9]+%", panelExtracted))[0]
    windSpeed = (re.findall("[A-Z]+ [0-9]+ mph", panelExtracted))[0]
    pressureRaw = (re.findall("Pressure[0-9]+\.*[0-9]*", panelExtracted))[0]
    pressure = (re.findall("[0-9]+\.*[0-9]*", pressureRaw))[0]

    #Add data to dictionary to return
    formattedResponse = {}
    formattedResponse["TempF"] = tempF
    formattedResponse["TempC"] = tempC
    formattedResponse["Description"] = phraseExtracted

    formattedResponse["Pressure"] = pressure + " in"
    formattedResponse["Humidity"] = humidity
    formattedResponse["WindSpeed"] = windSpeed

    return formattedResponse

#Gets the current weather at a certain zipcode in a specific country
def getCurrentWeatherAPI(zipCode, countryCode):
    completeUrl = (WEATHER_API_URL + "weather?" + "zip=" +
                    zipCode + "," + countryCode
                    + "&appid=" + OPEN_WEATHER_API_KEY)

    #Get data and extract in JSON format
    response = requests.get(completeUrl)
    jsonData = response.json()

    formattedResponse = {}

    #If valid html response
    if str(jsonData["cod"]) == "200":

        #Get a list of weather data by hour
        mainData = jsonData["main"]

        #Get temp, pressure, and humidity out of weather data
        currTemp = mainData["temp"]
        maxTemp = mainData["temp_max"]
        minTemp = mainData["temp_min"]
        currPres = mainData["pressure"]
        currHum = mainData["humidity"]

        #Get Weather Description
        weatherDescriptions = jsonData["weather"]
        weatherDesc = weatherDescriptions[0]["description"]

        #Get Wind Speed
        wind = jsonData["wind"]
        windSpeed = wind["speed"]

        #Add data to dictionary to return
        formattedResponse["TempF"] = (str(int((currTemp * (9/5) - 459.67)))
                                        + u" \N{DEGREE SIGN}F")
        formattedResponse["TempC"] = (str(round((currTemp - 273.15), 1))
                                        + u" \N{DEGREE SIGN}C")
        #Capitalize every word in the description
        formattedResponse["Description"] = \
    " ".join(list(map(lambda x: x.capitalize(), (weatherDesc.split(" ")))))

        formattedResponse["Pressure"] = str(currPres) + " hPa"
        formattedResponse["Humidity"] = str(currHum) + " %"
        formattedResponse["WindSpeed"] = (str(round((windSpeed * 2.236936), 1))
                                    + " mph")

        return formattedResponse

    else:
        raise Exception ("[!] Error #1: Could not access weather data cod: "
                            + str(jsonData["cod"]))

#If scrape for weather true then scrape else use api
def getWeather(zipCode, countryCode):
    if WEATHER_SCRAPE:
        return getTodaysWeatherScrape(zipCode, countryCode)
    else:
        return getCurrentWeatherAPI(zipCode, countryCode)
