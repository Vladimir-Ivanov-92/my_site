from django.db import models
from users.models import User


class Order(models.Model):
    CREATED = 0
    DELIVERED = 1

    STATUSES = [
        (CREATED, 'Создан'),
        (DELIVERED, 'Доставлен'),
    ]

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    address = models.CharField(max_length=256)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order #{self.id} {self.first_name} {self.last_name}"
