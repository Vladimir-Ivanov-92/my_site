from baskets.views import (basket_add, basket_add_auth, basket_remove,
                           basket_remove_auth)
from django.urls import path

urlpatterns = [
    path('basket/add/<slug:product_slug>/', basket_add, name="basket_add"),
    path('basket/add_auth/<slug:product_slug>/', basket_add_auth, name="basket_add_auth"),
    path('basket/remove/<int:basket_id>/', basket_remove, name="basket_remove"),
    path('basket/remove_auth/<int:basket_id>/', basket_remove_auth, name="basket_remove_auth"),

]
