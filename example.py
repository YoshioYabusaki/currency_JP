from decimal import Decimal
from bs4 import BeautifulSoup

import re

import requests


def round_currency(num) -> object:
    return Decimal(num).quantize(Decimal('.01'))

currency_url = 'https://alfabank.ua/currency-exchange'
response = requests.get(currency_url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')

rates = soup.find_all("h4", {"class": "exchange-rate-tabs__info-value"})

print(rates[0].text.strip())


# print(usd_buy, usd_sale, eur_buy, eur_sale)


# usd_buy = round_currency(rates[0].text) / 100
# usd_sale = round_currency(rates[1].text) / 100
# eur_buy = round_currency(rates[3].text) / 100
# eur_sale = round_currency(rates[4].text) / 100

# print(usd_buy, usd_sale, eur_buy, eur_sale)

# currency_url = 'https://www.oschadbank.ua/'
# response = requests.get(currency_url)
# response.raise_for_status()
# soup = BeautifulSoup(response.text, 'html.parser')
# rates = str(soup.findAll("span", {'class': ''}))
#
# my_list = re.sub(r"\D", " ", rates).split()
#
# usd_buy = float(my_list[4] + '.' + my_list[5])
# usd_sale = float(my_list[6] + '.' + my_list[7])
# eur_buy = float(my_list[0] + '.' + my_list[1])
# eur_sale = float(my_list[2] + '.' + my_list[3])
#
# breakpoint()
