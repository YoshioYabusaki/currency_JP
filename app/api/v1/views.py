from api.v1.filters import ContactUsFilter, RateFilter
from api.v1.paginators import ContactUsPagination, RatePagination
from api.v1.serializers import ContactUsSerializer, RateSerializer, SourceSerializer, SourceWithRateSerializer
from api.v1.throttles import AnonUserRateThrottle

from currency import model_choices as mch
from currency.models import ContactUs, Rate, Source

from django_filters import rest_framework as filters

from rest_framework import filters as rest_framework_filters
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response


class ContactUsViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all().order_by('-created')
    serializer_class = ContactUsSerializer
    pagination_class = ContactUsPagination
    filterset_class = ContactUsFilter
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
        rest_framework_filters.SearchFilter
    )
    ordering_fields = [
        'id',
        'created',
        'user_name',
        'email_form'
    ]
    search_fields = [
        'id',
        'user_name',
        'email_form',
        'subject',
    ]


class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all().select_related('source').order_by('-created')
    serializer_class = RateSerializer
    pagination_class = RatePagination
    filterset_class = RateFilter
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
    )
    ordering_fields = [
        'id',
        'created',
        'buy',
        'sale'
    ]
    throttle_classes = [AnonUserRateThrottle]


class RateChoicesView(generics.GenericAPIView):
    def get(self, request):
        return Response(
            {'rate_types': mch.RATE_TYPES},
        )


class SourceView(generics.ListAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class SourceWithRateView(generics.ListAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceWithRateSerializer
