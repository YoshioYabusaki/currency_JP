from currency.views import (
    contact_us_list, generate_password, good_cafe,
    index, rate_create, rate_delete, rate_details,
    rate_list, rate_update, response_codes,
    source_create, source_delete, source_details, source_list, source_update
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
    path('source/list/', source_list),
    path('source/create/', source_create),
    path('source/details/<int:source_id>/', source_details),  # idをパスの一部に↓
    path('source/update/<int:source_id>/', source_update),
    path('source/delete/<int:source_id>/', source_delete),
    path('contact/us/', contact_us_list),
    path('good/cafe/', good_cafe),
    path('response-codes/', response_codes)
]
