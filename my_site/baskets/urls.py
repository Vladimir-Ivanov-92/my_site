from django.urls import path

from baskets.views import (basket_add, basket_add_auth, basket_minus,
                           basket_minus_auth, basket_remove,
                           basket_remove_auth)

urlpatterns = [
    path('basket/add/<slug:product_slug>/', basket_add, name="basket_add"),
    path('basket/add_auth/<slug:product_slug>/', basket_add_auth, name="basket_add_auth"),
    path('basket/remove/<int:basket_id>/', basket_remove, name="basket_remove"),
    path('basket/remove_auth/<int:basket_id>/', basket_remove_auth, name="basket_remove_auth"),
    path('basket/minus/<slug:product_slug>/', basket_minus, name="basket_minus"),
    path('basket/minus_auth/<slug:product_slug>/', basket_minus_auth, name="basket_minus_auth"),

]
