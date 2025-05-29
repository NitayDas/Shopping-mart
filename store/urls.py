from django.urls import path
from . import views
from .views import RequestRefund,ItemRequestRefund

urlpatterns = [

        path('', views.store, name="store"),
        path('login/', views.login, name="login"),
        path('signup/', views.signup, name="signup"),
        path('logout/', views.logoutpage, name='logout'),
        path('cart/', views.cart, name="cart"),
        path('checkout/', views.checkout, name="checkout"),
        path('update_item/', views.updateItem, name="update_item"),
        path('order_info/', views.order_info, name="order_info"),
        path('process_order/', views.processOrder, name="process_order"),
        path('cancel_order/<int:order_id>/', views.cancel_order, name="cancel_order"),
        path('view_details/<int:order_id>/', views.view_details, name="view_details"),
        path('request-refund/<int:order_id>/', RequestRefund.as_view(), name='request-refund'),
        path('item_request-refund/<int:order_id>/<int:item_id>', ItemRequestRefund.as_view(), name='item_request-refund'),
        # path('deliver_order/<int:order_id>/', views.deliverOrder, name="deliver_order"),
        
]