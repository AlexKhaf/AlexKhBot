import requests
import json
from config import currencies


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты:\n -> {quote}')

        try:
            base_check = currencies[base]
        except KeyError:
            raise APIException(f'Неправильное наименование 1 валюты\n (для перевода) -> {base}')

        try:
            quote_check = currencies[quote]
        except KeyError:
            raise APIException(f'Неправильное наименование 2 валюты\n (в которую нужно перевести) ->  {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Количество указано не в цифровом формате:\n -> {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_check}&tsyms={quote_check}')
        total_base = json.loads(r.content)[currencies[quote]] * amount

        return round(total_base, 2)