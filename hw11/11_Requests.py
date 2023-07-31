import telebot
from telebot import types
import random
import json
from urllib import parse, request

bot = telebot.TeleBot('6398556781:AAFryWjf43cgi9cwGpP00fHaGZu7eFhJZU0')
@bot.message_handler(commands=['start'])
def start(message):
    # Створення клавіатури з кнопкою "👋 Say hi"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Say hi 👋")
    markup.add(btn1)

    # Відправлення вітання користувачу з клавіатурою
    bot.send_message(message.from_user.id, "👋 Hello! I'm your bot helper!", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Say hi 👋':
        # Створення клавіатури з новими кнопками
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Yes')
        btn2 = types.KeyboardButton('No')
        markup.add(btn1, btn2)
        
        # Відправлення питання та клавіатури з варіантами відповідей
        bot.send_message(message.from_user.id, 'Do you want to find gifs?', reply_markup=markup)

    elif message.text == 'Yes':
        # Відправлення відповіді користувачеві
        bot.send_message(message.from_user.id, 'Please enter the name of the gif you want to find:')
        bot.register_next_step_handler(message, process_gif_request)

    elif message.text == 'No':
        # Відправлення відповіді користувачеві
        bot.send_message(message.from_user.id, 'Bot is ending. Goodbye!')
        start(message)

def your_gif(name):
    url = "http://api.giphy.com/v1/gifs/search"
    params = parse.urlencode({
        "q": name,
        "api_key": "DHxdtVe5TMVWY87njn5cHhUvmqfePR9Z",
        "limit": "20"
    })
    a = random.randint(0,19)
    with request.urlopen("".join((url, "?", params))) as response:
        data = json.loads(response.read())
    try:
        gif_url = data["data"][a]["images"]["original"]["url"]
        return gif_url
    except:
        return False
def process_gif_request(message):
    gif_name = message.text
    gif_url = your_gif(gif_name)
    if gif_url==False:
        bot.send_message(message.from_user.id, 'Gif name doesn`t exsist. Do you want one more gif?')
    else:
        bot.send_message(message.from_user.id, gif_url)
        bot.send_message(message.from_user.id, 'Do you want one more gif?')

if __name__ == '__main__':
    bot.polling(none_stop=True)