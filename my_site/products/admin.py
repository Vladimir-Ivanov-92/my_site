from django.contrib import admin
from django.utils.safestring import mark_safe

from products.models import Category, Feature, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "image_show", "article", "name", "price", "category", "in_stock", "on_sale",
                    "time_create", "time_update")
    list_display_links = ("id", "article", "name")
    search_fields = ("name",)
    list_editable = ("on_sale", "in_stock")
    list_filter = ("in_stock", "on_sale", "category")
    prepopulated_fields = {"slug": ("name",)}

    def image_show(self, obj):
        if obj.image:
            return mark_safe("<img src='{}', width='60' />".format(obj.image.url))
        return None

    image_show.__name__ = "Картинка"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_display_links = ("name",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ("name_product", "shot_height", "time_work", "number_of_charges", "caliber")
    search_fields = ("name_product",)
