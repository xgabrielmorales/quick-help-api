# Django
from django.contrib import admin
from django.urls import path, include
# D.R.F Simple JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        "client/",
        include("quick_clients.api.urls")
    ),
    path(
        "product/",
        include("quick_products.api.urls")
    ),
    path(
        "bill/",
        include("quick_bills.api.urls")
    ),

    # TOKEN MANAGEMENT
    path(
        "api/token/",
        TokenObtainPairView.as_view(),
    ),
    path(
        "api/refresh/",
        TokenRefreshView.as_view(),
    ),
]
