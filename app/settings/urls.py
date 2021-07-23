from currency.views import (
    contact_us_list, generate_password, good_cafe,
    index, rate_list, response_codes, rate_create,
    rate_details, rate_update, rate_delete,
)

from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),

    # currency
    path('', index),
    path('gen-pass/', generate_password),
    path('rate/list/', rate_list),
    path('rate/create/', rate_create),
    path('rate/details/<int:rate_id>/', rate_details),
    path('rate/update/<int:rate_id>/', rate_update),
    path('rate/delete/<int:rate_id>/', rate_delete),
    path('contact/us/', contact_us_list),
    path('good/cafe/', good_cafe),
    path('response-codes/', response_codes)
]
