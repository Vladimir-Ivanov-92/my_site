from django.db import models

from products.models import Product
from users.models import User


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_amount(self):
        return sum(basket.amount for basket in self)


class BasketFK(models.Model):
    csrftoken = models.CharField(max_length=50, verbose_name="session_key", null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    amount = models.PositiveSmallIntegerField(default=0, verbose_name="Количество")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время заказа")

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f"Корзина для {self.csrftoken} | Продукт: {self.product}"

    def sum(self):
        return self.product.price * self.amount

    def de_json(self):
        basket_item = {
            'product_name': self.product.name,
            'amount': self.amount,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
        return basket_item

    class Meta:
        verbose_name = "КорзинаFK"
        verbose_name_plural = "КорзинаFK"
        ordering = ["time_create"]


class BasketAuth(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    amount = models.PositiveSmallIntegerField(default=0, verbose_name="Количество")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время заказа")

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f"Корзина для {self.user} | Продукт: {self.product}"

    def sum(self):
        return self.product.price * self.amount

    def de_json(self):
        basket_item = {
            'product_name': self.product.name,
            'amount': self.amount,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
        return basket_item

    class Meta:
        verbose_name = "КорзинаAuth"
        verbose_name_plural = "КорзинаAuth"
        ordering = ["time_create"]
