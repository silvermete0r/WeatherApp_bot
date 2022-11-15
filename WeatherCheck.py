import datetime as dt
import telebot
import Constant as const
from xml.dom.expatbuilder import FragmentBuilder
import requests

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

bot=telebot.TeleBot(const.TELEGRAM_API_KEY)

def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = round(kelvin - 273.1)
    fahrenheit = round(celsius * (9/5) + 32)
    return celsius, fahrenheit

@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(message.chat.id,"Hello, just send me the name of any city✌️")

@bot.message_handler(content_types='text')
def message_reply(message):
    CITY = message.text
    try:
        url = BASE_URL + "appid=" + const.WEATHER_API_KEY + "&q=" + CITY
        response = requests.get(url).json()
    
        temp_kelvin = response['main']['temp']
        temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
        feels_like_kelvin = response['main']['feels_like']
        feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
        wind_speed = response['wind']['speed']
        humidity = response['main']['humidity']
        description = response['weather'][0]['description']
        sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
        sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])
        bot.send_message(message.chat.id,f"Temperature in {CITY}: {temp_celsius:.2f}°C or {temp_fahrenheit:.2f}°F \nTemperature in {CITY} feels like: {feels_like_celsius:.2f}°C or {feels_like_fahrenheit:.2f}°F \nHumidity in {CITY}: {humidity}% \nWind Speed in {CITY}: {wind_speed}m/s \nGeneral Weather in {CITY}: {description} \nSun rises in {CITY} at {sunrise_time} local time.\nSun sets in {CITY} at {sunset_time} local time.")
    except:
        bot.send_message(message.chat.id, "Something went wrong, please type a valid city name!")
bot.infinity_polling()


