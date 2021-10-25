from api.v1 import views
from api.v1.views import SourceView, SourceWithRateView

from django.urls import path

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = 'api'

router = DefaultRouter()
router.register(r'rates', views.RateViewSet, basename='rate')
router.register(r'contactus', views.ContactUsViewSet, basename='contactus')

urlpatterns = [
    # path('contactus/', ContactUsView.as_view()),
    path('source/', SourceView.as_view(), name='source'),
    path('source_with_rate/', SourceWithRateView.as_view(), name='source_with_rate'),
    path('choices/', views.RateChoicesView.as_view(), name='currency_choices'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('rates/', views.RatesView.as_view()),
    # path('rates/<int:pk>/', views.RateDetailsView.as_view()),
]

urlpatterns.extend(router.urls)
