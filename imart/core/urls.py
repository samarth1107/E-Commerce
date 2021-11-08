from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name="homepage"),
    path('signup/', views.signup_view, name="buyer_signup"),
    path('login/', views.login_view, name="buyer_login"),   
    path('verification/', views.email_verification, name="buyer_verification"),
    path('otp_verification/<email>/', views.OTP_verification, name="buyer_otp_verification"),
    re_path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    path('add_to_cart/<product_id>/', views.add_to_cart, name="buyer_add_to_cart"),
    path('checkout/', views.checkout_page, name="buyer_checkout"),
    path('charge/', views.charge, name='buyer_charge'),
    path('user_profile/', views.user_profile, name="buyer_user_profile"),
    path('logout/', views.logout_view, name="buyer_logout"),
    path('browse_products/', views.browse_product, name="browse_product"),
    path('help/', views.help_page, name="help_page"),
]