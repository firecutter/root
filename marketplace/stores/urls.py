# 📁 Caminho: root/marketplace/stores/urls.py

from django.urls import path
from .views import StoreListPublicView, StoreDetailPublicView, MyStoreView

urlpatterns = [
    path("", StoreListPublicView.as_view(), name="store-list"),
    path("me/", MyStoreView.as_view(), name="store-me"),
    path("<slug:slug>/", StoreDetailPublicView.as_view(), name="store-detail"),
]