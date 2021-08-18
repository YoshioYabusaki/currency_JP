# import json
#
# from urllib import request
#
# from lxml import html
#

from currency import model_choices as mch

import requests
#
import urllib.request

from bs4 import BeautifulSoup

from decimal import Decimal

def round_currency(num):
    return Decimal(num).quantize(Decimal('.01'))

currency_url = 'https://ru.otpbank.com.ua/'
response = requests.get(currency_url)

response.raise_for_status()

source = 'otpbank'
soup = BeautifulSoup(response.text, 'html.parser')
data = soup.find("td", {"class": "currency-list__value"})

usd_buy = round_currency(data.text)
usd_sale = round_currency(data.next_element.next_element.next_element.text)
eur_buy = round_currency(data.next_element.next_element.next_element.next_element.next_element.next_element.
                         next_element.next_element.next_element.next_element.next_element.next_element.text)
eur_sale = round_currency(data.next_element.next_element.next_element.next_element.next_element.next_element.
                          next_element.next_element.next_element.next_element.next_element.next_element.
                          next_element.next_element.next_element.text)

currency_dict = {'ccy': mch.TYPE_USD, 'buy': usd_buy, 'sale': usd_sale}, \
                {'ccy': mch.TYPE_EUR, 'buy': eur_buy, 'sale': eur_sale}

for rate in currency_dict:
    ct = rate['ccy']
    buy = rate['buy']
    sale = rate['sale']

    print(ct, buy, sale)



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
## data = soup.find_all("div", {"id": "currency-table"})  # フォーマット：bs4.element.ResultSet
# del data["id"]
# print(data)
#
# new_data = data.strip("<div><currency-table :currencies='[" + "]'></currency-table></div>")

# print(new_data)
