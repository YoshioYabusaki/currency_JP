from decimal import Decimal

from bs4 import BeautifulSoup

from currency import model_choices as mch

import requests


def round_currency(num) -> object:
    return Decimal(num).quantize(Decimal('.01'))


currency_url = 'https://www.oschadbank.ua/'
response = requests.get(currency_url)

source = 'Ощадбанк'
soup = BeautifulSoup(response.text, 'html.parser')

rates = soup.find_all("span", {"class": "currency__item_value"})

for index, element in enumerate(rates):
    my_dict = {index: round_currency(element.text)}

    value_usd_buy = my_dict.get(2)
    if value_usd_buy is not None:
        usd_buy = value_usd_buy

    value_usd_sale = my_dict.get(3)
    if value_usd_sale is not None:
        usd_sale = value_usd_sale

        eur_buy = round_currency((soup.find("span", {"class": "currency__item_value"})).text)
        eur_sale = round_currency((soup.find("span", {"class": "currency__item_value"})).next_sibling.next_sibling.text)

        currency_dict = {'ccy': mch.TYPE_USD, 'buy': usd_buy, 'sale': usd_sale}, \
                        {'ccy': mch.TYPE_EUR, 'buy': eur_buy, 'sale': eur_sale}

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
