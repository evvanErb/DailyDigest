"""This file contains functions to scrap weather websites and format the
results for easy reading"""
#Python 3.x

import requests, json

with open ("passwords.txt", "r") as myfile:
    keysAndPasses = myfile.read()

keysAndPasses = eval(keysAndPasses)

#openweathermap.org

OPEN_WEATHER_API_KEY = keysAndPasses["OPEN_WEATHER_API_KEY"]
BASE_URL = "https://api.openweathermap.org/data/2.5/"

#Gets the current weather at a certain zipcode in a specific country
def getCurrentWeather(zipCode, countryCode):
    completeUrl = (BASE_URL + "weather?" + "zip=" + zipCode + "," + countryCode
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
