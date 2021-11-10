
import telebot
from config import TOKEN, exchanger
from extensions import Convertor, APIException


bot = telebot.TeleBot(TOKEN)  # создаем бота


@bot.message_handler(commands=['start', 'help'])  # обработчик команд /start, /help
def start(message: telebot.types.Message):
    text = "Приветсвую в конвертере валют!\n/value - список команд\nвалюта1 валюта2 сумма - перевод суммы из валюты1 в валюту2"

    bot.send_message(message.chat.id, text)  # ответ бота


@bot.message_handler(commands=['values'])  # обработчик команды /values
def values(message: telebot.types.Message):
    text = "Доступные валюты:\n"
    text += '\n'.join(exchanger.keys())  # формируем строку ответа

    bot.reply_to(message, text)  # ответ бота


@bot.message_handler(content_types=['text'])  # обработчик текста запроса на конвертацию
def converter(message: telebot.types.Message):
    values = message.text.split(' ')  # разделяем строку по пробелам
    values = list(map(str.lower, values))  # переводим строки в нижний регистр в список

    try:
        result = Convertor.get_price(values)  # если ошибка в конвертации
    except APIException as e:  # если ошибка пользователя
        bot.reply_to(message, f'Ошибка пользователя!\n{e}') # бот выдаст ошибку с сообщением
    except Exception as e:  # если ошибка программы
        bot.reply_to(message, f'Не удалось обработать команду...\n{e}')   # бот выдаст ошибку с сообщением
    else:
        text = f"{values[2]} {values[0]} = {result} {values[1]}"  # если все нормально формируем текст

        bot.reply_to(message, text)  # ответ бота


bot.polling(none_stop=True)  # запускаем бота
