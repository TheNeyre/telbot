import requests
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = open('token.txt').readline()
bot = telebot.TeleBot(TOKEN)
keyboard = InlineKeyboardMarkup(row_width=1)
keyboard.add(InlineKeyboardButton('Чаво за бот?!', callback_data='info'))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "Напишите мне название города в котором вы находитесь, я отправлю вам погоду!",
                     reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'info':
        bot.send_message(call.message.chat.id, "ЧаВо что да почему? 🤯😩😨\n---------------\nДля чего бот: пишите город - получите погоду в нём absolutly бесплатно\nАвтор: TheNeyre, ну Нарек крч\n вот и сказочке конец, а кто слушал - молодец!")

@bot.message_handler()
def get_weather(message):
    try:
        weather_descriptions = {
            "Clear": "Ясно ☀",
            "Clouds": "Облачно ☁",
            "Rain": "Дождь 🌧",
            "Drizzle": "Дождь 🌧",
            "Thunderstorm": "Гроза 🌩",
            "Snow": "Снег ❄",
            "Mist": "Туман 🌫"}
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&lang=ru&units=metric&appid=0971e3bb6ade6ef35bbd9ac470f1c41f")
        data = response.json()
        
        weather_description = data["weather"][0]["main"]
        if weather_description in weather_descriptions:
            wd = weather_descriptions[weather_description]
        else: wd = "непонятно..."
        bot.send_message(message.chat.id,
                    f"Город {data["name"]}\n-------------\nТемпература: {data['main']['temp']} - {wd} 🌡\nОщущается как: {data['main']['temp_min']} 🌌\nВлажность: {data["main"]["humidity"]}% 💧\nДавление: {data["main"]["pressure"]} мм.рт.ст ✈\nСкорость ветра: { data["wind"]["speed"]} м\с 🌪")
    except Exception as e: 
        bot.send_message(message.chat.id, 'Ой! Кажется вы ввели название города некоректно!')
        print(e)

if __name__ == "__main__": bot.infinity_polling()