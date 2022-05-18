import datetime
import re
from decimal import Decimal

from bs4 import BeautifulSoup

from celery import shared_task

from currency import consts
from currency import model_choices as mch
from currency.services import get_latest_rates

from django.conf import settings
from django.core.cache import cache
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
    from currency.models import Rate, Source  # タスク内でmodelsを使う場合はタスク内でインポートする

    alfa_currency_url = 'https://alfabank.ua/ru/currency-exchange'
    response = requests.get(alfa_currency_url)

    response.raise_for_status()  # raise error if status_code is not 2xx

    source = Source.objects.get_or_create(
        code_name=consts.CODE_NAME_ALFABANK,
        defaults={'name': 'alfabank'},
    )[0]
    soup = BeautifulSoup(response.text, 'html.parser')

    rates = soup.find_all("h4", {"class": "exchange-rate-tabs__info-value"})

    usd_buy = rates[0].text.strip()
    usd_sale = rates[1].text.strip()
    eur_buy = rates[2].text.strip()
    eur_sale = rates[3].text.strip()

    currency_dict = {'ccy': mch.TYPE_USD, 'buy': usd_buy, 'sale': usd_sale}, \
                    {'ccy': mch.TYPE_EUR, 'buy': eur_buy, 'sale': eur_sale}

    for rate in currency_dict:
        ct = rate['ccy']
        buy = round_currency(rate['buy'])  # str型からdecimal型に変換。DBがdecimal型だから。
        sale = round_currency(rate['sale'])

        last_rate = Rate.objects.filter(
            source=source,
            type=ct,
        ).order_by('created').last()

        if (
                last_rate is None or  # データベースが空の場合
                last_rate.buy != buy or  # buyに変化があった場合

                last_rate.sale != sale  # saleに変化があった場合
        ):
            Rate.objects.create(
                source=source,
                type=ct,
                buy=buy,
                sale=sale,
            )
            cache.delete(consts.CACHE_KEY_LATEST_RATES)
            get_latest_rates()


@shared_task
def parse_monobank():
    from currency.models import Rate, Source

    monobank_currency_url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(monobank_currency_url)

    response.raise_for_status()  # 結果が200番台ではないときにエラーを出す

    source = Source.objects.get_or_create(
        code_name=consts.CODE_NAME_MONOBANK,
        defaults={'name': 'monobank'},
    )[0]
    rates = response.json()

    for rate in rates:
        # USD-UAH or EUR-UAH
        if rate['currencyCodeB'] == 980 and (rate['currencyCodeA'] in (840, 978)):

            buy = round_currency(rate['rateBuy'])
            sale = round_currency(rate['rateSell'])

            ct = rate['currencyCodeA']
            if ct == 840:
                ct = mch.TYPE_USD
            if ct == 978:
                ct = mch.TYPE_EUR

            last_rate = Rate.objects.filter(
                source=source,
                type=ct,
            ).order_by('created').last()

            if (
                    last_rate is None or  # データベースが空の場合
                    last_rate.buy != buy or  # buyに変化があった場合
                    last_rate.sale != sale  # saleに変化があった場合
            ):
                Rate.objects.create(
                    source=source,
                    type=ct,
                    buy=buy,
                    sale=sale,
                )
                cache.delete(consts.CACHE_KEY_LATEST_RATES)
                get_latest_rates()


@shared_task
def parse_raiffeisenbank():
    from currency.models import Rate, Source

    currency_url = 'https://minfin.com.ua/company/aval/currency/'
    response = requests.get(currency_url)
    response.raise_for_status()

    source = Source.objects.get_or_create(
        code_name=consts.CODE_NAME_RAIFFEISENBANK,
        defaults={'name': 'Raiffeisenbank'},
    )[0]
    soup = BeautifulSoup(response.text, 'html.parser')

    rates = soup.find("table", {"class": "currency-data"})
    the_list = list(rates.findAll('td'))

    usd_buy = round_currency((the_list[5].text.replace("\n", ""))[0:5])
    usd_sale = round_currency((the_list[6].text.replace("\n", ""))[0:5])
    eur_buy = round_currency((the_list[9].text.replace("\n", ""))[0:5])
    eur_sale = round_currency((the_list[10].text.replace("\n", ""))[0:5])

    currency_dict = {'ccy': mch.TYPE_USD, 'buy': usd_buy, 'sale': usd_sale}, \
                    {'ccy': mch.TYPE_EUR, 'buy': eur_buy, 'sale': eur_sale}

    for rate in currency_dict:
        ct = rate['ccy']
        buy = rate['buy']
        sale = rate['sale']

        last_rate = Rate.objects.filter(
            source=source,
            type=ct,
        ).order_by('created').last()

        if (
                last_rate is None or
                last_rate.buy != buy or
                last_rate.sale != sale
        ):
            Rate.objects.create(
                source=source,
                type=ct,
                buy=buy,
                sale=sale,
            )
            cache.delete(consts.CACHE_KEY_LATEST_RATES)
            get_latest_rates()


@shared_task
def parse_ukrgasbank():
    from currency.models import Rate, Source

    currency_url = 'https://minfin.com.ua/company/ukrgasbank/currency/'
    response = requests.get(currency_url)

    source = Source.objects.get_or_create(
        code_name=consts.CODE_NAME_UKRGASBANK,
        defaults={'name': 'ukrgasbank'},
    )[0]
    soup = BeautifulSoup(response.text, 'html.parser')

    rates = soup.find("table", {"class": "currency-data"})
    the_list = list(rates.findAll('td'))

    usd_buy = round_currency((the_list[5].text.replace("\n", ""))[0:5])
    usd_sale = round_currency((the_list[6].text.replace("\n", ""))[0:5])
    eur_buy = round_currency((the_list[9].text.replace("\n", ""))[0:5])
    eur_sale = round_currency((the_list[10].text.replace("\n", ""))[0:5])

    currency_dict = {'ccy': mch.TYPE_USD, 'buy': usd_buy, 'sale': usd_sale}, \
                    {'ccy': mch.TYPE_EUR, 'buy': eur_buy, 'sale': eur_sale}

    for rate in currency_dict:
        ct = rate['ccy']
        buy = rate['buy']
        sale = rate['sale']

        last_rate = Rate.objects.filter(
            source=source,
            type=ct,
        ).order_by('created').last()

        if (
                last_rate is None or
                last_rate.buy != buy or
                last_rate.sale != sale
        ):
            Rate.objects.create(
                source=source,
                type=ct,
                buy=buy,
                sale=sale,
            )
            cache.delete(consts.CACHE_KEY_LATEST_RATES)
            get_latest_rates()


@shared_task
def parse_oschadbank():
    from currency.models import Rate, Source

    currency_url = 'https://www.oschadbank.ua/'
    response = requests.get(currency_url)
    response.raise_for_status()

    source = Source.objects.get_or_create(
        code_name=consts.CODE_NAME_OSCHADBANK,
        defaults={'name': 'oschadbank'},
    )[0]
    soup = BeautifulSoup(response.text, 'html.parser')

    rates = str(soup.findAll("span", {'class': ''}))
    my_list = re.sub(r"\D", " ", rates).split()

    usd_buy = round_currency(my_list[4] + '.' + my_list[5])
    usd_sale = round_currency(my_list[6] + '.' + my_list[7])
    eur_buy = round_currency(my_list[0] + '.' + my_list[1])
    eur_sale = round_currency(my_list[2] + '.' + my_list[3])

    currency_dict = {'ccy': mch.TYPE_USD, 'buy': usd_buy, 'sale': usd_sale}, \
                    {'ccy': mch.TYPE_EUR, 'buy': eur_buy, 'sale': eur_sale}

    for rate in currency_dict:
        ct = rate['ccy']
        buy = rate['buy']
        sale = rate['sale']

        last_rate = Rate.objects.filter(
            source=source,
            type=ct,
        ).order_by('created').last()

        if (
                last_rate is None or
                last_rate.buy != buy or
                last_rate.sale != sale
        ):
            Rate.objects.create(
                source=source,
                type=ct,
                buy=buy,
                sale=sale,
            )
            cache.delete(consts.CACHE_KEY_LATEST_RATES)
            get_latest_rates()


@shared_task
def parse_otpbank():
    from currency.models import Rate, Source  # タスク内でmodelsを使う場合はタスク内でインポートする

    currency_url = 'https://ru.otpbank.com.ua/'
    response = requests.get(currency_url)

    response.raise_for_status()

    source = Source.objects.get_or_create(
        code_name=consts.CODE_NAME_OTPBANK,
        defaults={'name': 'otpbank'},
    )[0]
    soup = BeautifulSoup(response.text, 'html.parser')
    rates = soup.findAll("td", {'class': 'currency-list__value'})

    usd_buy = round_currency(rates[0].text)
    usd_sale = round_currency(rates[2].text)
    eur_buy = round_currency(rates[1].text)
    eur_sale = round_currency(rates[3].text)

    currency_dict = {'ccy': mch.TYPE_USD, 'buy': usd_buy, 'sale': usd_sale}, \
                    {'ccy': mch.TYPE_EUR, 'buy': eur_buy, 'sale': eur_sale}

    for rate in currency_dict:
        ct = rate['ccy']
        buy = rate['buy']
        sale = rate['sale']

        last_rate = Rate.objects.filter(
            source=source,
            type=ct,
        ).order_by('created').last()

        if (
                last_rate is None or  # データベースが空の場合
                last_rate.buy != buy or  # buyに変化があった場合
                last_rate.sale != sale  # saleに変化があった場合
        ):
            Rate.objects.create(
                source=source,
                type=ct,
                buy=buy,
                sale=sale,
            )
            cache.delete(consts.CACHE_KEY_LATEST_RATES)
            get_latest_rates()


@shared_task
def parse_privatbank():
    from currency.models import Rate, Source  # タスク内でmodelsを使う場合はタスク内でインポートする

    privatbank_currency_url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response = requests.get(privatbank_currency_url)

    response.raise_for_status()  # raise error if status_code is not 2xx

    # source = 'privatbank'
    source = Source.objects.get_or_create(
        code_name=consts.CODE_NAME_PRIVATBANK,
        defaults={'name': 'PrivatBank'},
    )[0]
    rates = response.json()
    # available_currency_types = ('USD', 'EUR')
    available_currency_types = {
        'USD': mch.TYPE_USD,
        'EUR': mch.TYPE_EUR,
    }  # choiceにより、外部からの情報をシステム内部で使いやすいフォーマットに変換する

    for rate in rates:
        currency_type = rate['ccy']
        if currency_type in available_currency_types:

            buy = round_currency(rate['buy'])  # str型からdecimal型に変換。DBがdecimal型だから
            sale = round_currency(rate['sale'])
            ct = available_currency_types[currency_type]

            last_rate = Rate.objects.filter(
                source=source,
                type=ct,
            ).order_by('created').last()

            if (
                    last_rate is None or  # データベースが空の場合
                    last_rate.buy != buy or  # buyに変化があった場合
                    last_rate.sale != sale  # saleに変化があった場合
            ):
                Rate.objects.create(
                    source=source,
                    type=ct,
                    buy=buy,
                    sale=sale,
                )
                cache.delete(consts.CACHE_KEY_LATEST_RATES)
                get_latest_rates()


@shared_task
def parse_vkurse_dp_ua():
    from currency.models import Rate, Source

    currency_url = 'http://vkurse.dp.ua/course.json'
    response = requests.get(currency_url)

    response.raise_for_status()  # 結果が200番台ではないときにエラーを出す

    source = Source.objects.get_or_create(
        code_name=consts.CODE_NAME_VKURSE_DP_UA,
        defaults={'name': 'vkurse.dp.ua'},
    )[0]
    rates = response.json()
    # del rates["Rub"]

    usd_buy = re.sub(r"[^\d.]", "", rates['Dollar']['buy'])
    usd_sale = re.sub(r"[^\d.]", "", rates['Dollar']['sale'])
    eur_buy = re.sub(r"[^\d.]", "", rates['Euro']['buy'])
    eur_sale = re.sub(r"[^\d.]", "", rates['Euro']['sale'])  # emojiを削除

    currency_dict = {'ccy': mch.TYPE_USD, 'buy': usd_buy, 'sale': usd_sale}, \
                    {'ccy': mch.TYPE_EUR, 'buy': eur_buy, 'sale': eur_sale}

    for rate in currency_dict:
        ct = rate['ccy']
        buy = round_currency(rate['buy'])  # str型からdecimal型に変換。DBがdecimal型だから。
        sale = round_currency(rate['sale'])

        last_rate = Rate.objects.filter(
            source=source,
            type=ct,
        ).order_by('created').last()

        if (
                last_rate is None or  # データベースが空の場合
                last_rate.buy != buy or  # buyに変化があった場合
                last_rate.sale != sale  # saleに変化があった場合
        ):
            Rate.objects.create(
                source=source,
                type=ct,
                buy=buy,
                sale=sale,
            )
            cache.delete(consts.CACHE_KEY_LATEST_RATES)
            get_latest_rates()


@shared_task
def parse_privatbank_archive():
    from currency.models import Rate, Source  # タスク内でmodelsを使う場合はタスク内でインポートする

    source = Source.objects.get_or_create(
        code_name=consts.CODE_NAME_PRIVATBANK,
        defaults={'name': 'PrivatBank'},
    )[0]
    available_currency_types = {
        'USD': mch.TYPE_USD,
        'EUR': mch.TYPE_EUR,
    }

    def date_generator():
        from_date = datetime.datetime.today()
        while True:
            yield from_date  # 関数を一時的に実行停止できる。小分けにして返すことでメモリ消費量を節約する。
            from_date = from_date - datetime.timedelta(days=1)  # 今日から1日ずつ遡る

    for date_parsed in date_generator():
        if date_parsed.year == 2010:  # 昨日から2010年までの毎日
            break  # 2010年まで遡ったらストップ

        if not Rate.objects.filter(
                created__date=date_parsed,
                source=source,
                type__in=available_currency_types.values(),
        ).exists():  # filterに該当するオブジェクトでなければ下に進む

            date_for_url = {'date': f'{date_parsed.day}.{date_parsed.month}.{date_parsed.year}'}
            currency_url = requests.get(
                'https://api.privatbank.ua/p24api/exchange_rates?json',
                params=date_for_url
            )   # urlを生成する

            response = requests.get(currency_url.url)
            response.raise_for_status()
            rates = response.json()
            exchange_rates = rates['exchangeRate']

            for the_value in exchange_rates:
                if 'currency' in the_value:
                    currency_type = the_value['currency']
                    if currency_type in available_currency_types:
                        buy = round_currency(the_value['purchaseRate'])
                        sale = round_currency(the_value['saleRate'])
                        ct = available_currency_types[currency_type]

                        Rate.objects.create(
                            source=source,
                            type=ct,

                            buy=buy,
                            sale=sale,
                        )
                        the_rate = Rate.objects.last()
                        the_rate.created = date_parsed
                        the_rate.save()
                        print(f'object created: {date_parsed}')  # noqa

    # оригинальный вариант без исправления
    # создать список дат 'YYYY.mm.dd'
    # privatbank_rates = Rate.objects.filter(source=source).all()
    # existing_date_list = []
    # for the_rate in privatbank_rates:
    #     the_created_date = the_rate.created.strftime('%Y.%m.%d')
    #     if the_created_date not in existing_date_list:
    #         existing_date_list.append(the_created_date)
    #
    # d_today = datetime.date.today()
    # set_how_many_days = d_today - datetime.timedelta((365 * 4) + 1)  # 4 years (365 * 4) + 1
    # required_date_list = []
    # while d_today > set_how_many_days:
    #     required_date_list.append(set_how_many_days.strftime('%Y.%m.%d'))
    #     set_how_many_days = set_how_many_days + datetime.timedelta(1)
    #
    # target_date_list = sorted(list(set(required_date_list) - set(existing_date_list)))
    #
    # for the_date in target_date_list:
    #
    #     the_date_for_url = the_date[8:10] + '.' + the_date[5:7] + '.' + the_date[0:4]  # дата 'dd.mm.YYYY'
    #     currency_url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={the_date_for_url}'
    #
    #     response = requests.get(currency_url)
    #     response.raise_for_status()
    #     rates = response.json()
    #     exchange_rates = rates['exchangeRate']
    #
    #     for the_value in exchange_rates:
    #         if 'currency' in the_value:
    #             currency_type = the_value['currency']
    #             if currency_type in available_currency_types:
    #                 buy = round_currency(the_value['purchaseRate'])
    #                 sale = round_currency(the_value['saleRate'])
    #                 ct = available_currency_types[currency_type]
    #                 the_datetime = datetime.datetime.strptime(the_date, '%Y.%m.%d')
    #
    #                 Rate.objects.create(
    #                     source=source,
    #                     type=ct,
    #                     buy=buy,
    #                     sale=sale,
    #                 )
    #                 the_rate = Rate.objects.last()
    #                 the_rate.created = the_datetime
    #                 the_rate.save()
    #                 print(f'object created: {the_date}')  # noqa


# def parse_raiffeisenbank():
#     from currency.models import Rate, Source
#
#     currency_url = 'https://raiffeisen.ua/ru/'
#     response = requests.get(currency_url)
#     response.raise_for_status()
#
#     source = Source.objects.get_or_create(
#         code_name=consts.CODE_NAME_RAIFFEISENBANK,
#         defaults={'name': 'Raiffeisenbank'},
#     )[0]
#     soup = BeautifulSoup(response.text, 'html.parser')
#
#     rates = soup.find("div", {"id": "currency-table"})
#     text1 = str(rates.find('currency-table'))
#     list1 = re.sub(r"\D", " ", text1).split()
#
#     usd_buy = round_currency(list1[14] + '.' + list1[15])
#     usd_sale = round_currency(list1[16] + '.' + list1[17])
#     eur_buy = round_currency(list1[0] + '.' + list1[1])
#     eur_sale = round_currency(list1[2] + '.' + list1[3])
#
#     currency_dict = {'ccy': mch.TYPE_USD, 'buy': usd_buy, 'sale': usd_sale}, \
#                     {'ccy': mch.TYPE_EUR, 'buy': eur_buy, 'sale': eur_sale}
#
#     for rate in currency_dict:
#         ct = rate['ccy']
#         buy = rate['buy']
#         sale = rate['sale']
#
#         last_rate = Rate.objects.filter(
#             source=source,
#             type=ct,
#         ).order_by('created').last()
#
#         if (
#                 last_rate is None or
#                 last_rate.buy != buy or
#                 last_rate.sale != sale
#         ):
#             Rate.objects.create(
#                 source=source,
#                 type=ct,
#                 buy=buy,
#                 sale=sale,
#             )
#             cache.delete(consts.CACHE_KEY_LATEST_RATES)
#             get_latest_rates()


# @shared_task
# def debug_task(sleep_time: int = 5):
#
#     print(f'Count Rates: {Rate.objects.count()}')
# from time import sleep
# sleep(sleep_time)
# print(f'Task completed in {sleep_time}')
