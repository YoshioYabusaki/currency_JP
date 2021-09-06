import debug_toolbar

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', TemplateView.as_view(template_name='index.html'), name='index'),  # ここに作ればviewsに書く必要がない

    path('auth/', include('django.contrib.auth.urls')),  # ログイン・ログアウトなど
    # url('^', include('django.contrib.auth.urls')),  # 上記と同義

    path('currency/', include('currency.urls')),
    # ここには各種アプリのURL集を加える
    # currency.urlsにあるcurrency/で始まる全てのurlがここに集まる
    # これは書いた時点で、currency内のhtml内のurlsも書き変える必要がある。
    path('accounts/', include('accounts.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]

urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]

urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
