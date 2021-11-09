from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name="sellerAdminlogin"),
    path('sellerAdminhome/',views.home,name='sellerAdminhome'),
    path('sellerAdminlogout/', views.logout_view, name="sellerAdminlogout"),
    path('sellerAdminapprove/<username>/', views.approve, name="sellerAdminapprove"),
    path('sellerAdmindisapprove/<username>/', views.disapprove, name="sellerAdmindisapprove"),
    path('sellerAdminlistings/<username>/', views.listings, name="sellerAdminlistings"),
    path('sellerAdmindeleteProduct/<Product_id>/', views.deleteProduct, name="sellerAdmindeleteProduct"),
    path('sellerAdminchange_password/', views.change_password, name="sellerAdminchange_password"),
    path('sellerAdminDelete/<username>/', views.delete, name="sellerAdminDelete"),
    path('sellerAdminseller/', views.seller_view, name="sellerAdminseller"),
    path('sellerAdminbuyer/', views.buyer_view, name="sellerAdminbuyer"),
]