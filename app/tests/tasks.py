from currency.models import Rate
from currency.tasks import parse_monobank, parse_privatbank, parse_vkurse_dp_ua

from unittest.mock import MagicMock


def test_parse_vkurse(mocker):
    vkurse_response = [
        {
            "Dollar": {"buy": "26.30", "sale": "26.45"},
            "Euro": {"buy": "30.45", "sale": "30.60"},
            "Rub": {"buy": "0.357", "sale": "0.362"},
        }
    ]

    initial_count_rate = Rate.objects.count()
    requests_get_mock = mocker.patch('requests.get')  # 外部データを使わなくていいように。parse内でrequestsが使われない。
    requests_get_mock.return_value = MagicMock(json=lambda: vkurse_response[0])  # parse内のrequestsの返り値を定義する

    parse_vkurse_dp_ua()
    assert Rate.objects.count() == initial_count_rate + 2

    parse_vkurse_dp_ua()
    assert Rate.objects.count() == initial_count_rate + 2

    vkurse_response = [
        {
            "Dollar": {"buy": "26.30", "sale": "26.45"},
            "Euro": {"buy": "29.45", "sale": "30.60"},
        },
    ]
    requests_get_mock.return_value = MagicMock(json=lambda: vkurse_response[0])
    parse_vkurse_dp_ua()
    assert Rate.objects.count() == initial_count_rate + 3


def test_parse_monobank(mocker):
    monobank_response = [
        {"currencyCodeA": 840, "currencyCodeB": 980, "date": 1633503606, "rateBuy": 26.33, "rateSell": 26.5301},
        {"currencyCodeA": 978, "currencyCodeB": 980, "date": 1633503006, "rateBuy": 30.45, "rateSell": 30.7503},
    ]

    initial_count_rate = Rate.objects.count()
    requests_get_mock = mocker.patch('requests.get')  # 外部データを使わなくていいように。parse内でrequestsが使われない。
    requests_get_mock.return_value = MagicMock(json=lambda: monobank_response)  # parse内のrequestsの返り値を定義する

    parse_monobank()
    assert Rate.objects.count() == initial_count_rate + 2

    parse_monobank()
    assert Rate.objects.count() == initial_count_rate + 2

    monobank_response = [
        {"currencyCodeA": 840, "currencyCodeB": 980, "date": 1633503606, "rateBuy": 26.99, "rateSell": 27.5301},
    ]
    requests_get_mock.return_value = MagicMock(json=lambda: monobank_response)
    parse_monobank()
    assert Rate.objects.count() == initial_count_rate + 3


def test_parse_privatbank(mocker):
    privatbank_response = [
         {"ccy": "USD", "base_ccy": "UAH", "buy": "26.25000", "sale": "26.65000"},
         {"ccy": "EUR", "base_ccy": "UAH", "buy": "30.40000", "sale": "31.00000"},
         {"ccy": "RUR", "base_ccy": "UAH", "buy": "0.35000", "sale": "0.38000"},
         {"ccy": "BTC", "base_ccy": "USD", "buy": "46964.7304", "sale": "51908.3862"},
    ]

    initial_count_rate = Rate.objects.count()
    requests_get_mock = mocker.patch('requests.get')
    requests_get_mock.return_value = MagicMock(json=lambda: privatbank_response)

    parse_privatbank()
    assert Rate.objects.count() == initial_count_rate + 2

    parse_privatbank()
    assert Rate.objects.count() == initial_count_rate + 2

    privatbank_response = [
        {"ccy": "USD", "base_ccy": "UAH", "buy": "26.30000", "sale": "26.65000"},
    ]
    requests_get_mock.return_value = MagicMock(json=lambda: privatbank_response)
    parse_privatbank()
    assert Rate.objects.count() == initial_count_rate + 3
