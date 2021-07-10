from django.contrib import admin
from django.urls import path

from currency.views import hello_world, generate_password

urlpatterns = [
    path('admin/', admin.site.urls),

    # currency
    path('hello-world/', hello_world),
    path('gen-pass/', generate_password),
]
