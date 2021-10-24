from currency.models import Rate, Source


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


def test_put_invalid(api_client_auth):
    url = '/api/v1/rates/1/'
    json_data = {}
    response = api_client_auth.put(url, data=json_data)
    assert response.status_code == 400
    assert response.json() == {
        'source': ['This field is required.'],
        'buy': ['This field is required.'],
        'sale': ['This field is required.'],
    }


def test_put_valid(api_client_auth):
    rates_initial_count = Rate.objects.count()
    source = Source.objects.last()
    url = '/api/v1/rates/1/'
    json_data = {
        'source': source.pk,
        'buy': 29,
        'sale': 30,
    }
    response = api_client_auth.put(url, data=json_data)
    assert response.status_code == 200
    assert response.json()['buy'] == '29.00'
    assert response.json()['sale'] == '30.00'
    assert response.json()['type'] == 'USD'
    assert Rate.objects.count() == rates_initial_count


def test_delete_rates_invalid(api_client_auth):
    url = '/api/v1/rates/1000000/'
    response = api_client_auth.delete(url)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not found.'}


def test_delete_rates_valid(api_client_auth):
    rates_initial_count = Rate.objects.count()
    url = '/api/v1/rates/4/'
    response = api_client_auth.delete(url)
    assert response.status_code == 204
    assert Rate.objects.count() == rates_initial_count - 1
