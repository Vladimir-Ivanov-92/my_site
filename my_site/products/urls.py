from django.urls import path
from products.views import (CatalogView, CategoryView, HomeView, ProductView,
                            delivery_and_pay_page, feedback_page)

urlpatterns = [
    path('home', HomeView.as_view(), name="products_home"),
    path('catalog', CatalogView.as_view(), name="products_catalog"),
    path('category/<slug:category_slug>/', CategoryView.as_view(), name="category_page"),
    path('product/<slug:product_slug>/', ProductView.as_view(), name="product_page"),
    path('delivery_and_pay', delivery_and_pay_page, name="delivery_and_pay_page"),
    path('feedback', feedback_page, name="feedback_page"),
]
