from django.db import models
from django.urls import reverse


class Product(models.Model):
    article = models.CharField(max_length=15, verbose_name="Артикул")
    name = models.CharField(max_length=50, verbose_name="Наименование")
    slug = models.SlugField(max_length=75, unique=True, db_index=True, null=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to="image/%Y/%m/%d/", blank=True, verbose_name="Картинка")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    in_stock = models.BooleanField(default=False, verbose_name="В наличии")
    on_sale = models.BooleanField(default=False, verbose_name="В продаже")
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name="Категория")
    characteristic = models.ForeignKey('Feature', on_delete=models.PROTECT, null=True, verbose_name="Характеристика")

    def __str__(self):
        return f"{self.name}"

    def get_name(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_page', kwargs={"product_slug": self.slug})

    class Meta:
        verbose_name = "Товары"
        verbose_name_plural = "Товары"
        ordering = ["id"]


class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name="Наименование")
    slug = models.SlugField(max_length=75, unique=True, db_index=True, null=True, verbose_name="URL")

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('category_page', kwargs={"category_slug": self.slug})

    class Meta:
        verbose_name = "Категории"
        verbose_name_plural = "Категории"
        ordering = ["id"]


class Feature(models.Model):
    name_product = models.CharField(max_length=50, verbose_name="Наименование продукта", null=True, blank=True)
    shot_height = models.DecimalField(max_digits=5, decimal_places=2, null=True, verbose_name="Высота выстрела (м)")
    time_work = models.PositiveIntegerField(null=True, verbose_name="Время работы (сек)")
    number_of_charges = models.PositiveIntegerField(null=True, verbose_name="Количество зарядов (шт)")
    caliber = models.PositiveIntegerField(null=True, verbose_name="Калибр (мм)")

    def __str__(self):
        return f"Характеристика для: {self.name_product}"

    class Meta:
        verbose_name = "Характеристики"
        verbose_name_plural = "Характеристики"
        ordering = ["id"]
