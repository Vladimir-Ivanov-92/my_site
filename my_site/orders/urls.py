from django.urls import path

from orders.views import (OrderCreateView, OrderDetailView, OrderIsCreateView,
                          OrdersListForStaffView, OrdersListView)

urlpatterns = [
    path('order_create/', OrderCreateView.as_view(), name="order_create"),
    path('', OrdersListView.as_view(), name="orders_list"),
    path('order/<int:pk>/', OrderDetailView.as_view(), name="order_detail"),
    path('order_is_create/<int:pk>/', OrderIsCreateView.as_view(), name="order_is_create"),
    path('orders_for_staff/', OrdersListForStaffView.as_view(), name="orders_for_staff"),

]
