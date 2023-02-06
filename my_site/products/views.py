from django.core.cache import cache
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from products.models import Category, Product
from products.utils import DataMixin


class HomeView(DataMixin, ListView):
    model = Product
    template_name = 'products/home.html'
    context_object_name = "products"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(context_def.items()))


class CatalogView(DataMixin, ListView):
    model = Product
    template_name = 'products/catalog.html'
    context_object_name = "products"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title="Каталог")
        return dict(list(context.items()) + list(context_def.items()))

    def get_success_url(self):
        return reverse_lazy('products_home')


class CategoryView(DataMixin, ListView):
    model = Product
    template_name = 'products/catalog.html'
    context_object_name = "products"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title=Category.objects.get(slug=self.kwargs["category_slug"]).name,
                                            category_selected=Category.objects.get(
                                                slug=self.kwargs["category_slug"]).id)
        return dict(list(context.items()) + list(context_def.items()))

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs["category_slug"], on_sale=True)


class ProductView(DataMixin, DetailView):
    model = Product
    template_name = 'products/product.html'
    slug_url_kwarg = "product_slug"
    context_object_name = "product"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title=context["product"].name,
                                            category_selected=context["product"].category_id)
        context_cache = cache.get_or_set('context_def', context_def, 30)
        return dict(list(context.items()) + list(context_cache.items()))


def feedback_page(request):
    return HttpResponse("feedback_page")


def delivery_and_pay_page(request):
    return HttpResponse("dostavka_and_pay_page")
