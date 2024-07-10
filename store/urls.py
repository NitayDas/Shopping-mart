from django.urls import path
from . import views

urlpatterns = [

        path('', views.store, name="store"),
        path('login/', views.login, name="login"),
        path('signup/', views.signup, name="signup"),
        path('logout/', views.logoutpage, name='logout'),
        path('cart/', views.cart, name="cart"),
        path('update_item/', views.updateItem, name="update_item"),
        path('checkout/', views.checkout, name="checkout"),
]