from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="homepage"),
    path('signup/', views.signup_view, name="buyer_signup"),
    path('login/', views.login_view, name="buyer_login"),
    path('logout/', views.logout_view, name="buyer_logout"),
    path('browse_products/', views.browse_product, name="browse_product"),
]