from currency import consts
from currency import model_choices as mch
from currency.models import Rate, Source

from django.core.cache import cache


def get_latest_rates():
    latest_rates = cache.get(consts.CACHE_KEY_LATEST_RATES)
    if latest_rates is not None:
        return latest_rates

    rates = []
    for source in Source.objects.all():
        for currency_type, _ in mch.RATE_TYPES:

            rate = Rate.objects \
                .filter(source=source, type=currency_type) \
                .order_by('-created').first()

            if rate is not None:
                rates.append(rate)

    cache.set(consts.CACHE_KEY_LATEST_RATES, rates, 60 * 60 * 24 * 14)
    return rates
