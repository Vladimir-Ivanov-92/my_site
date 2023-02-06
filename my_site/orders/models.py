from django.db import models

from baskets.models import BasketAuth, BasketFK
from users.models import User


class Order(models.Model):
    CREATED = 0
    IN_WORK = 1
    DELIVERED = 2

    STATUSES = [
        (CREATED, 'Создан'),
        (IN_WORK, 'В работе'),
        (DELIVERED, 'Доставлен'),
    ]

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    address = models.CharField(max_length=256)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return f"Order #{self.id} {self.first_name} {self.last_name}"

    def update_after_oder(self, csrftoken=None):
        if not self.initiator:
            baskets = BasketFK.objects.filter(csrftoken=csrftoken)
        else:
            baskets = BasketAuth.objects.filter(user=self.initiator)
        self.status = self.IN_WORK
        self.basket_history = {
            'order_items': [basket.de_json() for basket in baskets],
            'total_sum': float(baskets.total_sum()),
        }
        baskets.delete()
        self.save()
