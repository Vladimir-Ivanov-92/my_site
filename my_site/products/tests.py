from http import HTTPStatus

from django.http import SimpleCookie
from django.test import TestCase
from django.urls import reverse

from products.models import Category, Product


class HomeViewTestCase(TestCase):

    def test_view(self):
        self.client.cookies = SimpleCookie({'csrftoken': 'csrftoken'})
        path = reverse('products_home')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Главная страница')
        self.assertTemplateUsed(response, 'products/home.html')


class CatalogViewTestCase(TestCase):
    fixtures = ['categories.json', 'feature.json', 'product.json']

    def setUp(self):
        self.products = Product.objects.all()

    def test_list(self):
        self.client.cookies = SimpleCookie({'csrftoken': 'csrftoken'})
        path = reverse('products_catalog')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Каталог')
        self.assertTemplateUsed(response, 'products/catalog.html')
        self.assertEqual(list(response.context_data['products']), list(self.products[:6]))


class CategoryViewTestCase(TestCase):
    fixtures = ['categories.json', 'feature.json', 'product.json']

    def test_list_with_category(self):
        self.client.cookies = SimpleCookie({'csrftoken': 'csrftoken'})

        category = Category.objects.first()
        path = reverse('category_page', kwargs={"category_slug": category.slug})
        response = self.client.get(path)
        title = Category.objects.first().name

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], title)
        self.assertTemplateUsed(response, 'products/catalog.html')
        self.assertEqual(list(response.context_data['products']),
                         list(Product.objects.filter(category__slug=category.slug))
                         )


class ProductViewTestCase(TestCase):
    fixtures = ['categories.json', 'feature.json', 'product.json']

    def test_product_page(self):
        self.client.cookies = SimpleCookie({'csrftoken': 'csrftoken'})

        product = Product.objects.first()
        path = reverse('product_page', kwargs={"product_slug": product.slug})
        response = self.client.get(path)
        title = Product.objects.first().name

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], title)
        self.assertTemplateUsed(response, 'products/product.html')
        self.assertEqual(response.context_data['product'],
                         Product.objects.get(slug=product.slug)
                         )
