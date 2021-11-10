

import json
import requests
from config import  exchanger


class APIException(Exception):
    pass


class Convertor:
    @staticmethod  # статический метод класса
    def get_price(values):  # функция принимает список
        if len(values) != 3:  # если длина списка неравна 3
            raise APIException("Неверное количество параметров!")  # Ошибка

        quote, base, amount = values  # распоковываем список в три переменные

        if quote == base:  # если переменные равны
            raise APIException(f"Невозможно перевезти одинаковые валюты {base}")  # вызываем ощибку

        try:
            quote_formatted = exchanger[quote]  # если значение ключа не найдено
        except KeyError:
            raise APIException(f"Не возможно обработать валюту {quote}")  # выдаем ошибку

        try:
            base_formatted = exchanger[base]  # если значение ключа не найдено
        except KeyError:
            raise APIException(f"Не возможно обработать валюту {base}")  # выдаем ошибку

        try:
            amount = float(amount)  # если значение не переводится в вещественное число
        except KeyError:
            raise APIException(f"Не возможно обработать количество {amount}")  # выдаем ошибку

        # если все нормально переходим к запросу курса валют с сайта
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_formatted}&tsyms={base_formatted}')  # запрос курса валют
        res = json.loads(r.content)[base_formatted]  # загружаем в json и получаем значение по ключу
        total = round((res * amount), 2)  # результат умножаем на значение и округляем до 2 значений, после запятой

        return total  # возвращаем сконвертированный результат
