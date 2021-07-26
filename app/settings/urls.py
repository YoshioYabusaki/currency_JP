import debug_toolbar
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', TemplateView.as_view(template_name='index.html'), name='index'),  # ここに作ればviewsに書く必要がない

    # ここには他のアプリのURL集を加える
    path('currency/', include('currency.urls')),  # currency.urlsにあるcurrency/で始まる全てのurlがここに集まる

    path('__debug__/', include(debug_toolbar.urls)),
]
