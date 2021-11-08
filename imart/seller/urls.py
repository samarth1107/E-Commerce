from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name="login"),
    path('signup/', views.signup_view,name="signup"),
    path('Sellerhome/',views.home,name='Sellerhome'),
    path('Sellerlogout/', views.logout_view, name="Sellerlogout"),
    path('Selleradd_product/', views.add_product, name='Selleradd_product'),
    path('Selleredit-product/<int:pk>/', views.edit_product, name='Selleredit_product'),
    path('Sellerdelete_product/<int:pk>', views.delete_product, name="Sellerdelete_product"),
    path('Sellerchange_password/', views.change_password, name="Sellerchange_password"),
    path('otp_verification/<email>/', views.OTP_verification, name="seller_otp_verification")
]