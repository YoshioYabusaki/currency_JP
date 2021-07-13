from currency.views import contact_us_list, generate_password, hello_world, rate_list

from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),

    # currency
    path('hello-world/', hello_world),
    path('gen-pass/', generate_password),
    path('rate/list/', rate_list),
    path('contact/us/', contact_us_list),
]
