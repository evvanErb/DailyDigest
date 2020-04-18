"""This file contains functions to scrap news websites and format the
results for easy reading"""
#Python 3.x

import requests, json

#newsapi.org

with open ("passwords.txt", "r") as myfile:
    keysAndPasses = myfile.read()

keysAndPasses = eval(keysAndPasses)
NEWS_API_KEY = keysAndPasses["NEWS_API_KEY"]
BASE_URL = "http://newsapi.org/v2/top-headlines?"

def getMajorHeadlines():
    countryCode = "us"

    completeUrl = (BASE_URL + "country=" + countryCode +
                "&apiKey=" + NEWS_API_KEY)

    #Get data and extract in JSON format
    response = requests.get(completeUrl)
    jsonData = response.json()

    formattedResponse = []

    if str(jsonData["status"]) == "ok":
        numResults = str(jsonData["totalResults"])

        articles = jsonData["articles"]

        #Iterate over all the articles
        for article in articles:
            currentArticle = {}

            #Get all the info for current article
            sourceInfo = article["source"]
            author = article["author"]
            title = article["title"]
            description = article["description"]
            url = article["url"]
            urlToImage = article["urlToImage"]
            publishDate = article["publishedAt"]
            content = article["content"]

            #Add to dictionary of data for current article
            currentArticle["SourceID"] = sourceInfo["id"]
            currentArticle["SourceName"] = sourceInfo["name"]
            currentArticle["Title"] = title
            currentArticle["Description"] = description
            currentArticle["Url"] = url
            currentArticle["UrlToImage"] = urlToImage
            currentArticle["PublishDate"] = publishDate
            currentArticle["Content"] = content

            #Add current article data to list of article data
            formattedResponse.append(currentArticle)

        return formattedResponse

    else:
        raise Exception ("[!] Error #1: Could not access weather data cod: "
                            + str(jsonData["status"]))
