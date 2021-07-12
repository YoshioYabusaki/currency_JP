from currency.views import generate_password, hello_world

from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),

    # currency
    path('hello-world/', hello_world),
    path('gen-pass/', generate_password),
]
