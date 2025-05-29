from django.urls import path
from . import views

urlpatterns = [
       path("admin_view/", views.Admin_view, name="admin_view"),
       path('update_product/<int:id>/', views.update_product, name='update_product'),
       path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
       path('refund_lists/', views.Refund_List, name='refund_lists'),
       path('approve_request/<int:refun_id>/' ,views.approve_request, name='approve_request'),
       path('item_approve_request/<int:refun_id>/' ,views.item_approve_request, name='item_approve_request'),
]