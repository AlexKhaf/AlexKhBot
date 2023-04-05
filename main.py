import telebot
from config import currencies, TOKEN
from extensions import APIException, Converter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Для начала работы введите команду боту в формате:\n<имя валюты>\n \
<в какую валюту перевести>\n \
<количество валюты>\n \
-------------------\n \
Увидеть список всех доступных валют: /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currencies.keys():
        text  += '\n' + key
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()

        if len(values) != 3:
            raise APIException('Количество параметров не равно 3!')

        base, quote, amount = values
        base, quote = base.lower(), quote.lower()
        amount = amount.replace(',','.')

        total_base = Converter.get_price(base, quote, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя!\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Системная ошибка! Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
