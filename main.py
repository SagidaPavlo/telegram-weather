import telebot
import requests
import config
import re
from bs4 import BeautifulSoup as BS

bot = telebot.TeleBot('1885545186:AAF7-GBMHslMckFHBA6MQtwa1jWC5jP9flY')

weather_re = re.compile("Погода в (?P<city>[А-яЫіїІЇ`'-a-zA-Z]+)")


def get_weather(city):
    r = requests.get('https://ua.sinoptik.ua/погода-' + city)
    html = BS(r.content, 'html.parser')

    for el in html.select('#content'):
        t_min = el.select('.temperature .min')[0].text
        t_max = el.select('.temperature .max')[0].text
        text = el.select('.wDescription .description')[0].text

        return {'min': t_min, 'max': t_max, 'desc': text}

    return {}

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привіт":
        bot.send_message(message.from_user.id, "Привіт, я вмію знаходити прогноз погоди на завтра.")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши Привіт")
    elif message.text == "/start":
        bot.send_message("Привіт))")
    elif weather_re.match(message.text):
        try:
            result = get_weather(weather_re.match(message.text).groupdict()['city'])
        except Exception:
            bot.send_message(message.from_user.id, 'Сталася помилка, спробуйте пізніше')
        else:
            if 'desc' in result:
                bot.send_message(message.from_user.id, f'{result["desc"]}. {result["min"]}, {result["max"]}')
            else:
                bot.send_message(message.from_user.id, 'Такого міста не знайдено')
    else:
        bot.send_message(message.from_user.id, "Вв")

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
