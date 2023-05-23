import telebot
import requests
from telebot.types import Message


def read_token() -> str:
    with open('./token.txt', "r") as file_in:
        token = file_in.read().removesuffix('\n')
        return token
    
API_TOKEN = read_token()
bot = telebot.TeleBot(API_TOKEN)
CITY_POS = {
    'Tomsk': (56.4977, 84.9744)
    }


def get_temperature(city_name: str):
    city_data = CITY_POS[city_name.title()]
    response = requests.get('https://api.open-meteo.com/v1/forecast?latitube={city_data[0]}&longitube={city_data[1]}&current_weather=true')
    if response.status_code == 200:
        weather_data = response.json()
        return weather_data['current_weather']['temperature']
    else:
        return None

def get_weather(city_name: str):
    response = requests.get(f'https://wttr.in/{city_name}?format=3')
    if response.status_code == 200:
        return response.text
    return None

@bot.message_handler(commands=['start'])
def command_start(msg):
    bot.send_message(msg.chat.id, 'Привет, я VladBot, чем смогу тебе помочь?')

@bot.message_handler(commands=['help'])
def command_help(message):
    bot.send_message(message.chat.id, 'Меня создал Влад Киселев, который научился создавать мне подобных ;)')

@bot.message_handler(commands=['weather'])
def command_weather(Msg):
    bot.send_message(Msg.chat.id, get_weather('Томск'))

bot.polling(non_stop=True)
