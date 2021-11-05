from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="homepage"),
    path('browse_products/', views.browse_product, name="browse_product"),
]