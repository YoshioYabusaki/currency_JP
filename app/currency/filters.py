import django_filters

from currency.models import Rate

from django.forms import DateInput


class RateFilter(django_filters.FilterSet):

    created_gte = django_filters.DateFilter(
        widget=DateInput(attrs={'type': 'date'}),
        field_name='created',
        lookup_expr='date__gte',  # created__date__gte
    )

    created_lte = django_filters.DateFilter(
        widget=DateInput(attrs={'type': 'date'}),
        field_name='created',
        lookup_expr='date__lte',  # created__date__lte
    )

    class Meta:
        model = Rate
        fields = {
            'type': ('exact', ),
            'buy': ('exact', ),
            'sale': ('exact', ),
        }
