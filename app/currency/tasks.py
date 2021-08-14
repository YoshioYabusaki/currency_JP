from decimal import Decimal

from bs4 import BeautifulSoup

from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail

import requests


def round_currency(num):
    return Decimal(num).quantize(Decimal('.01'))


@shared_task
def contact_us(subject, body):
    send_mail(
        subject,
        body,
        settings.EMAIL_HOST_USER,  # от кого
        [settings.SUPPORT_EMAIL],  # получатель
        fail_silently=False,
    )


@shared_task
def parse_alfabank():
    from currency.models import Rate  # タスク内でmodelsを使う場合はタスク内でインポートする

    alfa_currency_url = 'https://alfabank.ua/ru'
    response = requests.get(alfa_currency_url)

    response.raise_for_status()  # raise error if status_code is not 2xx

    source = 'alfabank'
    soup = BeautifulSoup(response.text, 'html.parser')

    usd_buy = round_currency(soup.find("span", {"data-currency": "USD_BUY"}).text.strip())
    usd_sale = round_currency(soup.find("span", {"data-currency": "USD_SALE"}).text.strip())
    eur_buy = round_currency(soup.find("span", {"data-currency": "EUR_BUY"}).text.strip())
    eur_sale = round_currency(soup.find("span", {"data-currency": "EUR_SALE"}).text.strip())

    currency_dict = {'ccy': 'USD', 'buy': usd_buy, 'sale': usd_sale}, \
                    {'ccy': 'EUR', 'buy': eur_buy, 'sale': eur_sale}

    for rate in currency_dict:
        currency_type = rate['ccy']

        buy = rate['buy']
        sale = rate['sale']

        last_rate = Rate.objects.filter(
            source=source,
            type=currency_type,
        ).order_by('created').last()

        if (
                last_rate is None or  # データベースが空の場合
                last_rate.buy != buy or  # buyに変化があった場合
                last_rate.sale != sale  # saleに変化があった場合
        ):
            Rate.objects.create(
                source=source,
                type=currency_type,
                buy=buy,
                sale=sale,
            )


@shared_task
def parse_monobank():
    from currency.models import Rate

    monobank_currency_url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(monobank_currency_url)

    response.raise_for_status()  # 結果が200番台ではないときにエラーを出す

    source = 'monobank'
    rates = response.json()

    for rate in rates:
        # USD-UAH or EUR-UAH
        if rate['currencyCodeB'] == 980 and (rate['currencyCodeA'] in (840, 978)):

            buy = round_currency(rate['rateBuy'])
            sale = round_currency(rate['rateSell'])

            currency_type = rate['currencyCodeA']
            if currency_type == 840:
                currency_type = 'USD'
            if currency_type == 978:
                currency_type = 'EUR'

            last_rate = Rate.objects.filter(
                source=source,
                type=currency_type,
            ).order_by('created').last()

            if (
                    last_rate is None or  # データベースが空の場合
                    last_rate.buy != buy or  # buyに変化があった場合
                    last_rate.sale != sale  # saleに変化があった場合
            ):
                Rate.objects.create(
                    source=source,
                    type=currency_type,
                    buy=buy,
                    sale=sale,
                )


@shared_task
def parse_oschadbank():
    from currency.models import Rate

    currency_url = 'https://www.oschadbank.ua/ua'
    response = requests.get(currency_url)

    response.raise_for_status()

    source = 'Ощадбанк'
    soup = BeautifulSoup(response.text, 'html.parser')

    usd_buy = round_currency(soup.find("strong", {"class": "buy-USD"}).text.strip())
    usd_sale = round_currency(soup.find("strong", {"class": "sell-USD"}).text.strip())
    eur_buy = round_currency(soup.find("strong", {"class": "buy-EUR"}).text.strip())
    eur_sale = round_currency(soup.find("strong", {"class": "sell-EUR"}).text.strip())

    currency_dict = {'ccy': 'USD', 'buy': usd_buy, 'sale': usd_sale}, \
                    {'ccy': 'EUR', 'buy': eur_buy, 'sale': eur_sale}

    for rate in currency_dict:
        currency_type = rate['ccy']

        buy = rate['buy']
        sale = rate['sale']

        last_rate = Rate.objects.filter(
            source=source,
            type=currency_type,
        ).order_by('created').last()

        if (
                last_rate is None or
                last_rate.buy != buy or
                last_rate.sale != sale
        ):
            Rate.objects.create(
                source=source,
                type=currency_type,
                buy=buy,
                sale=sale,
            )


@shared_task
def parse_otpabank():
    from currency.models import Rate  # タスク内でmodelsを使う場合はタスク内でインポートする

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

    currency_dict = {'ccy': 'USD', 'buy': usd_buy, 'sale': usd_sale}, \
                    {'ccy': 'EUR', 'buy': eur_buy, 'sale': eur_sale}

    for rate in currency_dict:
        currency_type = rate['ccy']

        buy = rate['buy']
        sale = rate['sale']

        last_rate = Rate.objects.filter(
            source=source,
            type=currency_type,
        ).order_by('created').last()

        if (
                last_rate is None or  # データベースが空の場合
                last_rate.buy != buy or  # buyに変化があった場合
                last_rate.sale != sale  # saleに変化があった場合
        ):
            Rate.objects.create(
                source=source,
                type=currency_type,
                buy=buy,
                sale=sale,
            )


@shared_task
def parse_privatbank():
    from currency.models import Rate  # タスク内でmodelsを使う場合はタスク内でインポートする

    privatbank_currency_url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response = requests.get(privatbank_currency_url)

    response.raise_for_status()  # raise error if status_code is not 2xx

    source = 'privatbank'
    rates = response.json()
    available_currency_types = ('USD', 'EUR')  # 読みやすくするために

    for rate in rates:
        currency_type = rate['ccy']
        if currency_type in available_currency_types:

            buy = round_currency(rate['buy'])  # str型からdecimal型に変換。DBがdecimal型だから。
            sale = round_currency(rate['sale'])

            last_rate = Rate.objects.filter(
                source=source,
                type=currency_type,
            ).order_by('created').last()

            if (
                    last_rate is None or  # データベースが空の場合
                    last_rate.buy != buy or  # buyに変化があった場合
                    last_rate.sale != sale  # saleに変化があった場合
            ):
                Rate.objects.create(
                    source=source,
                    type=currency_type,
                    buy=buy,
                    sale=sale,
                )


@shared_task
def parse_vkurse_dp_ua():
    from currency.models import Rate

    currency_url = 'http://vkurse.dp.ua/course.json'
    response = requests.get(currency_url)

    response.raise_for_status()  # 結果が200番台ではないときにエラーを出す

    source = 'vkurse.dp.ua'
    rates = response.json()
    del rates['Rub']

    usd_buy = rates['Dollar']['buy']
    usd_sale = rates['Dollar']['sale']
    eur_buy = rates['Euro']['buy']
    eur_sale = rates['Euro']['sale']

    currency_dict = {'ccy': 'USD', 'buy': usd_buy, 'sale': usd_sale}, \
                    {'ccy': 'EUR', 'buy': eur_buy, 'sale': eur_sale}

    for rate in currency_dict:
        currency_type = rate['ccy']

        buy = round_currency(rate['buy'])  # str型からdecimal型に変換。DBがdecimal型だから。
        sale = round_currency(rate['sale'])

        last_rate = Rate.objects.filter(
            source=source,
            type=currency_type,
        ).order_by('created').last()

        if (
                last_rate is None or  # データベースが空の場合
                last_rate.buy != buy or  # buyに変化があった場合
                last_rate.sale != sale  # saleに変化があった場合
        ):
            Rate.objects.create(
                source=source,
                type=currency_type,
                buy=buy,
                sale=sale,
            )


# @shared_task
# def debug_task(sleep_time: int = 5):
#
#     print(f'Count Rates: {Rate.objects.count()}')
    # from time import sleep
    # sleep(sleep_time)
    # print(f'Task completed in {sleep_time}')
