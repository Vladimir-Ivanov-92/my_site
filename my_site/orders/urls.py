from django.urls import path

from orders.views import OrderCreateView, OrderDetailView, OrdersListView

urlpatterns = [
    path('order_create/', OrderCreateView.as_view(), name="order_create"),
    path('', OrdersListView.as_view(), name="orders_list"),
    path('order/<int:pk>/', OrderDetailView.as_view(), name="order_detail"),

]
