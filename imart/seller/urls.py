from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name="login"),
    path('signup/', views.signup_view,name="signup"),
    path('home/',views.home,name='home'),
    path('logout/', views.logout_view, name="logout"),
    path('add_product/', views.add_product, name='add_product'),
    path('edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:pk>', views.delete_product, name="delete_product"),
    #path('approve/<username>/', views.approve, name="approve"),
    #path('disapprove/<username>/', views.disapprove, name="disapprove"),
    #path('listings/<username>/', views.listings, name="listings"),
    #path('deleteProduct/<Product_id>/', views.deleteProduct, name="deleteProduct"),
]