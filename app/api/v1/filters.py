from currency.models import ContactUs, Rate

from django_filters import rest_framework as filters


class RateFilter(filters.FilterSet):

    class Meta:
        model = Rate
        fields = {
            'buy': ('lt', 'lte', 'gt', 'gte', 'exact'),
            'sale': ('lt', 'lte', 'gt', 'gte', 'exact'),
        }


class ContactUsFilter(filters.FilterSet):

    class Meta:
        model = ContactUs
        fields = {
            'user_name': ('startswith', 'endswith', 'contains', 'exact'),
            'email_form': ('startswith', 'endswith', 'contains', 'exact'),
            'subject': ('startswith', 'endswith', 'contains', 'exact'),
            'message': ('startswith', 'endswith', 'contains', 'exact'),
        }
