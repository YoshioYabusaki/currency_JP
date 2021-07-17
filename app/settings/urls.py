from currency.views import contact_us_list, generate_password, index, rate_list, response_codes

from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),

    # currency
    path('', index),
    path('gen-pass/', generate_password),
    path('rate/list/', rate_list),
    path('contact/us/', contact_us_list),
    path('response-codes/', response_codes)
]
