from django.urls import path

from products.views import (CatalogTableView, CatalogView, CategoryTableView,
                            CategoryView, HomeView, ProductView,
                            delivery_and_pay_page, feedback_page)

urlpatterns = [
    path('home', HomeView.as_view(), name="products_home"),
    path('catalog/', CatalogView.as_view(), name="products_catalog"),
    path('catalog_table/', CatalogTableView.as_view(), name="products_table_catalog"),
    path('category/<slug:category_slug>/', CategoryView.as_view(), name="category_page"),
    path('category_table/<slug:category_slug>/', CategoryTableView.as_view(), name="category_table_page"),
    path('product/<slug:product_slug>/', ProductView.as_view(), name="product_page"),
    path('delivery_and_pay', delivery_and_pay_page, name="delivery_and_pay_page"),
    path('feedback', feedback_page, name="feedback_page"),
]
