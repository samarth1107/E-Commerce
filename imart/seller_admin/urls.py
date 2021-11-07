from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name="login"),
    path('home/',views.home,name='home'),
    path('logout/', views.logout_view, name="logout"),
    path('approve/<username>/', views.approve, name="approve"),
    path('disapprove/<username>/', views.disapprove, name="disapprove"),
    path('listings/<username>/', views.listings, name="listings"),
    path('deleteProduct/<Product_id>/', views.deleteProduct, name="deleteProduct"),
]