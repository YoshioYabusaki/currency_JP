import debug_toolbar

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework import permissions


schema_view = get_schema_view(
   openapi.Info(
      title="Open Rates API",
      default_version='v1',
      description="Current Bank Rates",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', TemplateView.as_view(template_name='index.html'), name='index'),  # ここに作ればviewsに書く必要がない

    path('auth/', include('django.contrib.auth.urls')),  # ログイン・ログアウトなど
    # url('^', include('django.contrib.auth.urls')),  # 上記と同義

    path('currency/', include('currency.urls')),
    # ここには各種アプリのURL集を加える
    # currency.urlsにあるcurrency/で始まる全てのurlがここ↑に集まる
    # これは書いた時点で、currency内のhtml内のurlsも書き変える必要がある。
    path('accounts/', include('accounts.urls')),
    path('api/v1/', include('api.v1.urls')),
    path('__debug__/', include(debug_toolbar.urls)),

    # API docs
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]

urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
