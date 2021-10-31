from decimal import Decimal

from currency import model_choices as mch, consts

from currency.models import Rate, Source

# from bs4 import BeautifulSoup

# import re

import requests

import datetime


def round_currency(num) -> object:
    return Decimal(num).quantize(Decimal('.01'))








source = Source.objects.get_or_create(
        code_name=consts.CODE_NAME_PRIVATBANK,
        defaults={'name': 'PrivatBank'},
    )[0]
available_currency_types = {
    'USD': mch.TYPE_USD,
    'EUR': mch.TYPE_EUR,
}

privatbank_rates = Rate.objects.filter(source=source).all()
existing_date_list = []
for the_rate in privatbank_rates:
    created_date = the_rate.created.strftime('%Y.%m.%d')
    if created_date not in existing_date_list:
        existing_date_list.append(created_date)

d_today = datetime.date.today()  # 今日を定義
set_how_many_days = d_today - datetime.timedelta(20)  # 本番(365 * 4) + 1
required_date_list = []
while d_today > set_how_many_days:
    required_date_list.append(set_how_many_days.strftime('%Y.%m.%d'))
    set_how_many_days = set_how_many_days + datetime.timedelta(1)

target_date_list = sorted(list(set(required_date_list) - set(existing_date_list)))

for the_date in target_date_list:
    currency_url = [f'https://api.privatbank.ua/p24api/exchange_rates?json&date={the_date}']
    breakpoint()

    print(currency_url)



# while access_date < d_today:
#     the_date = (access_date.strftime('%d.%m.%Y'))  # 日付を文字列に変換
#     currency_url = [f'https://api.privatbank.ua/p24api/exchange_rates?json&date={the_date}']
#
#     for the_url in currency_url:
#         response = requests.get(the_url)
#         response.raise_for_status()
#
#         rates = response.json()
#         exchange_rates = rates['exchangeRate']
#
#         for the_value in exchange_rates:
#             if 'currency' in the_value:
#                 currency_type = the_value['currency']
#                 if currency_type in available_currency_types:
#                     buy = round_currency(the_value['purchaseRate'])
#                     sale = round_currency(the_value['saleRate'])
#                     ct = available_currency_types[currency_type]
#                     print(the_date, source, ct, buy, sale)
#
#         access_date = access_date + datetime.timedelta(1)






# d_today = datetime.date.today()  # 今日を定義
# four_years_ago = d_today - datetime.timedelta(2)  # 本番(365 * 4) + 1
#
# source = 'privat'
# available_currency_types = {
#     'USD': mch.TYPE_USD,
#     'EUR': mch.TYPE_EUR,
# }
#
# access_date = four_years_ago
# print(access_date)
# while access_date < d_today:
#     the_date = (access_date.strftime('%d.%m.%Y'))  # 日付を文字列に変換
#     currency_url = [
#         f'https://api.privatbank.ua/p24api/exchange_rates?json&date={the_date}'
#     ]
#
#     for the_url in currency_url:
#         response = requests.get(the_url)
#         response.raise_for_status()
#
#         rates = response.json()
#         exchange_rates = rates['exchangeRate']
#         del exchange_rates[0]
#
#         for the_value in exchange_rates:
#             currency_type = the_value['currency']
#             if currency_type in available_currency_types:
#                 buy = round_currency(the_value['purchaseRate'])
#                 sale = round_currency(the_value['saleRate'])
#                 ct = available_currency_types[currency_type]
#                 print(the_date, source, ct, buy, sale)
#
#     access_date = access_date + datetime.timedelta(1)

###################################################
# currency_url = 'https://www.oschadbank.ua/'
# response = requests.get(currency_url)
#
# source = 'Ощадбанк'
# soup = BeautifulSoup(response.text, 'html.parser')
#
# rates = soup.find_all("span", {"class": "currency__item_value"})
#
# for index, element in enumerate(rates):
#     my_dict = {index: round_currency(element.text)}
#
#     value_usd_buy = my_dict.get(2)
#     if value_usd_buy is not None:
#         usd_buy = value_usd_buy
#
#     value_usd_sale = my_dict.get(3)
#     if value_usd_sale is not None:
#         usd_sale = value_usd_sale
#
#         eur_buy = round_currency((soup.find("span", {"class": "currency__item_value"})).text)
#         eur_sale = round_currency(
#         (soup.find("span", {"class": "currency__item_value"})).next_sibling.next_sibling.text
#         )
#
#         currency_dict = {'ccy': mch.TYPE_USD, 'buy': usd_buy, 'sale': usd_sale}, \
#                         {'ccy': mch.TYPE_EUR, 'buy': eur_buy, 'sale': eur_sale}

# print(currency_dict)

# rates = soup.find_all("span", {"class": "currency__item_value"})
# for element in rates:
#     the_data = element.find("span")
#     for this in the_data:
#         print(this[0])


# test_list = ['a', 'b', 'c', 'd', 'e']
# print(test_list[3])

# for index, element in enumerate(test_list):
#     data = element
#     print(data[1])


# usd_buy = round_currency(soup.find("strong", {"class": "buy-USD"}).text.strip())
# usd_sale = round_currency(soup.find("strong", {"class": "sell-USD"}).text.strip())
# eur_buy = round_currency(soup.find("strong", {"class": "buy-EUR"}).text.strip())
# eur_sale = round_currency(soup.find("strong", {"class": "sell-EUR"}).text.strip())
#
# currency_dict = {'ccy': mch.TYPE_USD, 'buy': usd_buy, 'sale': usd_sale}, \
#                 {'ccy': mch.TYPE_EUR, 'buy': eur_buy, 'sale': eur_sale}
#
# for rate in currency_dict:
#     ct = rate['ccy']
#     buy = rate['buy']
#     sale = rate['sale']
#
#     print(ct, buy, sale)


# currency_url = 'https://www.universalbank.com.ua/ru'
# response = requests.get(currency_url)
#
# soup = BeautifulSoup(response.text, 'html.parser')
# data = soup.find_all("td", {"class": "p-b-xs-2 p-y-1-sm"})
# print(data)


# currency_url = 'https://www.pumb.ua/ru/'
# response = requests.get(currency_url)
#
# soup = BeautifulSoup(response.content, 'html.parser')
# data = soup.find("div", {"class": "rates-block"})


# for element in data:
#     my_value = element.text  # str型
# my_value = element.text.split(" ")  # list型


# currency_url = 'https://raiffeisen.ua/ru'
# response = requests.get(currency_url)
#
# soup = BeautifulSoup(response.text, 'html.parser')
# data = soup.find('div', id="currency-table")
#
# jsonData = json['currencies']
#
#
# the_tag = data.next_element.next_element  # bs4.element.Tag


# html = urllib.request.urlopen(currency_url)
# soup = BeautifulSoup(html, 'html.parser')
#
# data = soup.find(id="currency-table")  # フォーマット：bs4.element.Tag
# data = soup.find_all("div", {"id": "currency-table"})  # フォーマット：bs4.element.ResultSet
# del data["id"]
# print(data)
#
# new_data = data.strip("<div><currency-table :currencies='[" + "]'></currency-table></div>")

# print(new_data)

# rates = {
#     'date': '01.12.2014',
#     'bank': 'PB',
#     'baseCurrency': 980,
#     'baseCurrencyLit': 'UAH',
#     'exchangeRate':
#     [
#         {'baseCurrency': 'UAH', 'currency': 'AUD', 'saleRateNB': 12.831925, 'purchaseRateNB': 12.831925},
#         {'baseCurrency': 'UAH', 'currency': 'USD', 'saleRateNB': 15.056413, 'purchaseRateNB': 15.056413,
#         'saleRate': 15.7, 'purchaseRate': 15.35},
#         {'baseCurrency': 'UAH', 'currency': 'EUR', 'saleRateNB': 18.79492, 'purchaseRateNB': 18.79492,
#         'saleRate': 20.0, 'purchaseRate': 19.2},
#         {'baseCurrency': 'UAH', 'currency': 'PLZ', 'saleRateNB': 4.492201, 'purchaseRateNB': 4.492201,
#         'saleRate': 5.0, 'purchaseRate': 4.2}
#     ]
# }
#
# exchange_rates = rates['exchangeRate']
# for the_data in exchange_rates:
#     print(the_data['currency'])

the_dict = [
    {'baseCurrency': 'UAH', 'saleRateNB': 19.7289, 'purchaseRateNB': 19.7289},
    {'baseCurrency': 'UAH', 'currency': 'AZN', 'saleRateNB': 15.662, 'purchaseRateNB': 15.662},
    {'baseCurrency': 'UAH', 'currency': 'BYN', 'saleRateNB': 10.8978, 'purchaseRateNB': 10.8978},
    {'baseCurrency': 'UAH', 'currency': 'CAD', 'saleRateNB': 21.3186, 'purchaseRateNB': 21.3186},
    {'baseCurrency': 'UAH', 'currency': 'CHF', 'saleRateNB': 28.6688, 'purchaseRateNB': 28.6688, 'saleRate': 29.2, 'purchaseRate': 27.6},
    {'baseCurrency': 'UAH', 'currency': 'CNY', 'saleRateNB': 4.1236, 'purchaseRateNB': 4.1236},
    {'baseCurrency': 'UAH', 'currency': 'CZK', 'saleRateNB': 1.1889, 'purchaseRateNB': 1.1889, 'saleRate': 1.3, 'purchaseRate': 1.1},
    {'baseCurrency': 'UAH', 'currency': 'DKK', 'saleRateNB': 4.1098, 'purchaseRateNB': 4.1098},
    {'baseCurrency': 'UAH', 'currency': 'EUR', 'saleRateNB': 30.5749, 'purchaseRateNB': 30.5749, 'saleRate': 30.85, 'purchaseRate': 30.25},
    {'baseCurrency': 'UAH', 'currency': 'GBP', 'saleRateNB': 36.2496, 'purchaseRateNB': 36.2496, 'saleRate': 37.2, 'purchaseRate': 35.2},
    {'baseCurrency': 'UAH', 'currency': 'HUF', 'saleRateNB': 0.083577, 'purchaseRateNB': 0.083577},
    {'baseCurrency': 'UAH', 'currency': 'ILS', 'saleRateNB': 8.2218, 'purchaseRateNB': 8.2218},
    {'baseCurrency': 'UAH', 'currency': 'JPY', 'saleRateNB': 0.23173, 'purchaseRateNB': 0.23173},
    {'baseCurrency': 'UAH', 'currency': 'KZT', 'saleRateNB': 0.061954, 'purchaseRateNB': 0.061954},
    {'baseCurrency': 'UAH', 'currency': 'MDL', 'saleRateNB': 1.5081, 'purchaseRateNB': 1.5081},
    {'baseCurrency': 'UAH', 'currency': 'NOK', 'saleRateNB': 3.1517, 'purchaseRateNB': 3.1517},
    {'baseCurrency': 'UAH', 'currency': 'PLN', 'saleRateNB': 6.6218, 'purchaseRateNB': 6.6218, 'saleRate': 6.81, 'purchaseRate': 6.51},
    {'baseCurrency': 'UAH', 'currency': 'RUB', 'saleRateNB': 0.3772, 'purchaseRateNB': 0.3772, 'saleRate': 0.389, 'purchaseRate': 0.36},
    {'baseCurrency': 'UAH', 'currency': 'SEK', 'saleRateNB': 3.0582, 'purchaseRateNB': 3.0582},
    {'baseCurrency': 'UAH', 'currency': 'SGD', 'saleRateNB': 19.5583, 'purchaseRateNB': 19.5583},
    {'baseCurrency': 'UAH', 'currency': 'TMT', 'saleRateNB': 7.605, 'purchaseRateNB': 7.605},
    {'baseCurrency': 'UAH', 'currency': 'TRY', 'saleRateNB': 2.7277, 'purchaseRateNB': 2.7277},
    {'baseCurrency': 'UAH', 'currency': 'UAH', 'saleRateNB': 1.0, 'purchaseRateNB': 1.0},
    {'baseCurrency': 'UAH', 'currency': 'USD', 'saleRateNB': 26.3509, 'purchaseRateNB': 26.3509, 'saleRate': 26.65, 'purchaseRate': 26.25},
    {'baseCurrency': 'UAH', 'currency': 'UZS', 'saleRateNB': 0.0024895, 'purchaseRateNB': 0.0024895},
    {'baseCurrency': 'UAH', 'currency': 'GEL', 'saleRateNB': 8.5403, 'purchaseRateNB': 8.5403}
]

# my_dict = {'baseCurrency': 'UAH', 'saleRateNB': 19.8407, 'purchaseRateNB': 19.8407},\
#           {'baseCurrency': 'UAH', 'currency': 'AZN', 'saleRateNB': 15.662, 'purchaseRateNB': 15.662},\
#           {'baseCurrency': 'UAH', 'currency': 'BYN', 'saleRateNB': 10.9482, 'purchaseRateNB': 10.9482}
#
# print(my_dict['baseCurrency'])
# currency_type = [d.get('currency') for d in my_dict]
# print(currency_type)
