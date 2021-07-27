from currency.views import (
    GeneratePasswordView,
    RateCreateView, RateDeleteView, RateDetailView, RateListView, RateUpdateView,
    contact_us_list, good_cafe, response_codes,
    SourceCreateView, SourceDeleteView, SourceDetailView, SourceListView, SourceUpdateView
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

    path('contact/us/', contact_us_list),
    path('good/cafe/', good_cafe),
    path('response-codes/', response_codes),
    path('gen-pass/', GeneratePasswordView.as_view()),

    # path('rate/list/', rate_list),
    # path('rate/create/', rate_create),
    # path('rate/details/<int:rate_id>/', rate_details),
    # path('rate/update/<int:rate_id>/', rate_update),
    # path('rate/delete/<int:rate_id>/', rate_delete),
]
