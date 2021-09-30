from currency.views import (
    ContactUsCreateView, ContactUsListView, GeneratePasswordView, GoodCafeListView,
    RateCreateView, RateDeleteView, RateDetailView, RateListView, RateUpdateView,
    SourceCreateView, SourceDeleteView, SourceDetailView, SourceListView, SourceUpdateView,
    response_codes,
    # rates_list_api_example,
)

from django.urls import path

app_name = 'currency'

urlpatterns = [
    path('rate/list/', RateListView.as_view(), name='rate-list'),  # 最後に.as_view()を付けるのはルール
    path('rate/create/', RateCreateView.as_view(), name='rate-create'),  # nameによってパスを得るやり方 → ここでパスを自由に編集できるようになる。
    path('rate/details/<int:pk>/', RateDetailView.as_view(), name='rate-details'),  # 以前は<int:rate_id>と書いたが、pkと書くルール
    path('rate/update/<int:pk>/', RateUpdateView.as_view(), name='rate-update'),  # これら三つを最初から書くようになろう
    path('rate/delete/<int:pk>/', RateDeleteView.as_view(), name='rate-delete'),

    path('source/list/', SourceListView.as_view(), name='source-list'),
    path('source/create/', SourceCreateView.as_view(), name='source-create'),
    path('source/details/<int:pk>/', SourceDetailView.as_view(), name='source-details'),  # idをパスの一部に↓<int:pk>
    path('source/update/<int:pk>/', SourceUpdateView.as_view(), name='source-update'),
    path('source/delete/<int:pk>/', SourceDeleteView.as_view(), name='source-delete'),

    path('contact/us/', ContactUsListView.as_view(), name='contact-us-list'),
    path('contact/us/create/', ContactUsCreateView.as_view(), name='contact-us-create'),

    path('good/cafe/', GoodCafeListView.as_view(), name='good-cafe-list'),
    path('response-codes/', response_codes),  # パス名とviewsで作った関数名
    path('gen-pass/', GeneratePasswordView.as_view()),

    # API
    # path('api/rate/list/', rates_list_api_example),

    # path('rate/list/', rate_list),
    # path('rate/create/', rate_create),
    # path('rate/details/<int:rate_id>/', rate_details),
    # path('rate/update/<int:rate_id>/', rate_update),
    # path('rate/delete/<int:rate_id>/', rate_delete),
]
