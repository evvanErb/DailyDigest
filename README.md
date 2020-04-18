# DailyDigest
Emails users the current weather,
 top news stories,
 and stock index data daily at 10:00 system time

Written in Python 3.x

Uses newsapi.org for top news stories,
 openweathermap.org for current weather,
 and alphavantage.co for stock data.

 Can Web Scrape for weather data in which case it scrapes weather.com for
 weather data instead of using openweathermap.org

Uses requests, json, smtplib, email, schedule, datetime,
 bs4, re, & time libraries

To Run: python3 main.py
