from currency.models import Rate, Source

from django.urls import reverse


def test_get_rates(api_client_auth):
    url = '/api/v1/rates/'
    response = api_client_auth.get(url)
    assert response.status_code == 200
    assert response.json()


def test_post_invalid(api_client_auth):
    url = '/api/v1/rates/'
    response = api_client_auth.post(url, json={})
    assert response.status_code == 400  # что-то не то отправили(
    assert response.json() == {
        'source': ['This field is required.'],
        'buy': ['This field is required.'],
        'sale': ['This field is required.'],
    }


def test_post_valid(api_client_auth):
    rates_initial_count = Rate.objects.count()
    source = Source.objects.last()
    url = '/api/v1/rates/'
    json_data = {
        'source': source.pk,
        'buy': 27,
        'sale': 28,
    }
    response = api_client_auth.post(url, data=json_data)
    assert response.status_code == 201
    assert response.json()['buy'] == '27.00'
    assert response.json()['sale'] == '28.00'
    assert response.json()['type'] == 'USD'
    assert Rate.objects.count() == rates_initial_count + 1


def test_put_valid(api_client_auth):
    source = Source.objects.last()
    url = '/api/v1/rates/1/'

    json_data = {
        'source': source.pk,
        'buy': 27,
        'sale': 28,
    }
    response = api_client_auth.put(url, data=json_data)
    breakpoint()


# my_data = {
#       "id": 230,
#       "source_obj": {
#         "id": 1,
#         "name": "alfabank",
#       },
#       "type": "USD",
#       "buy": "24.00",
#       "sale": "25.00",
#       "created": "2021-10-07T11:37:39.082140+03:00",
#     }


# このurlが実際のdbにつながっているかどうか解明すべし
    # その可否でオブジェクトの定義の仕方が異なってくる