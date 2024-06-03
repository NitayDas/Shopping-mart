from django.urls import path
from . import views

urlpatterns = [

        path('', views.store, name="store"),
        path('login/', views.login, name="login"),
        path('signup/', views.signup, name="signup"),
        path('logout/', views.logoutpage, name='logout'),
]