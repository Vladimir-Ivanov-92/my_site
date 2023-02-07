from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField

from baskets.models import BasketAuth, BasketFK
from orders.telegram import send_message_about_order_in_telegram
from users.models import User


class Order(models.Model):
    TEMPORARY = 0
    CREATED = 1
    IN_WORK = 2
    DELIVERED = 3
    CANCELLED = 4

    STATUSES = [
        (TEMPORARY, 'Временный'),
        (CREATED, 'Создан'),
        (IN_WORK, 'В работе'),
        (DELIVERED, 'Доставлен'),
        (CANCELLED, 'Отменен'),
    ]

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    phone_number = PhoneNumberField(null=True, default=None)
    address = models.CharField(max_length=256)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=TEMPORARY, choices=STATUSES)
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    csrftoken = models.CharField(max_length=256, null=True, default=None)

    def __str__(self):
        return f"Order #{self.id} {self.first_name} {self.last_name}"

    def send_order_mail(self):
        subject = f"Создан заказ №{self.id}"
        link = reverse('orders_for_staff')
        orders_for_staff_link = f"{settings.DOMAIN_NAME}{link}"
        message_for_staff_on_email = (
            f"Покупатель:\n"
            f"Имя: {self.first_name} \n"
            f"Фамилия: {self.last_name} \n"
            f"Телефон: {self.phone_number.as_international} \n"
            f"Электронная почта: {self.email} \n"
            f"Адрес доставки: {self.address} \n \n"
            f"Заказ №{self.id}:\n"
            f"Общая сумма заказа: {self.basket_history['total_sum']}руб. \n"
            f"Перейти на страницу заказов: {orders_for_staff_link} \n\n"
            f"#Товары в заказе: \n"
        )

        message_for_staff_on_telegram = (
            f"Покупатель:\n"
            f"Имя: {self.first_name} \n"
            f"Фамилия: {self.last_name} \n"
            f"Телефон: {self.phone_number} \n"
            f"Электронная почта: {self.email} \n"
            f"Адрес доставки: {self.address} \n \n"
            f"Заказ №{self.id}:\n"
            f"Общая сумма заказа: {self.basket_history['total_sum']}руб. \n"
            f"Перейти на страницу заказов: {orders_for_staff_link} \n\n"
            f"#Товары в заказе: \n"
        )

        message_for_user_on_email = (
            f"Спасибо за оформленный заказ на сайте {settings.DOMAIN_NAME} \n"
            f"В ближайшее время мы свяжемся с Вами для уточнения данных по заказу и согласования времени доставки.\n\n"
            f"Данные вашего заказа:\n"
            f"Имя: {self.first_name} \n"
            f"Фамилия: {self.last_name} \n"
            f"Телефон: {self.phone_number} \n"
            f"Электронная почта: {self.email} \n"
            f"Адрес доставки: {self.address} \n \n"
            f"Заказ №{self.id}:\n"
            f"Общая сумма заказа: {self.basket_history['total_sum']}руб. \n"
            f"#Товары в заказе: \n"
        )

        for i in range(self.basket_history['order_items'].__len__()):
            message_for_staff_on_email += (
                f"#{i + 1} "
                f"{self.basket_history['order_items'][i]['product_name']}| "
                f"Количество: {self.basket_history['order_items'][i]['amount']}шт.| "
                f"Цена за шт: {self.basket_history['order_items'][i]['price']}руб.| "
                f"Всего: {self.basket_history['order_items'][i]['sum']}руб. \n\n"
            )

            message_for_staff_on_telegram += (
                f"#{i + 1} "
                f"{self.basket_history['order_items'][i]['product_name']}| "
                f"Количество: {self.basket_history['order_items'][i]['amount']}шт.| "
                f"Цена за шт: {self.basket_history['order_items'][i]['price']}руб.| "
                f"Всего: {self.basket_history['order_items'][i]['sum']}руб. \n\n"
            )

            message_for_user_on_email += (
                f"#{i + 1} "
                f"{self.basket_history['order_items'][i]['product_name']}| "
                f"Количество: {self.basket_history['order_items'][i]['amount']}шт.| "
                f"Цена за шт: {self.basket_history['order_items'][i]['price']}руб.| "
                f"Всего: {self.basket_history['order_items'][i]['sum']}руб. \n\n"
            )

        send_message_about_order_in_telegram(message_for_staff_on_telegram)
        # send mail for staff about order:
        send_mail(
            subject=subject,
            message=message_for_staff_on_email,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_STAFF],
            fail_silently=False,
        )
        # send mail for user about order:
        send_mail(
            subject=subject,
            message=message_for_user_on_email,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.email],
            fail_silently=False,
        )

    def update_after_oder(self, csrftoken=None):
        if not self.initiator:
            baskets = BasketFK.objects.filter(csrftoken=csrftoken)
        else:
            baskets = BasketAuth.objects.filter(user=self.initiator)
        self.status = self.CREATED
        self.basket_history = {
            'order_items': [basket.de_json() for basket in baskets],
            'total_sum': float(baskets.total_sum()),
        }
        baskets.delete()
        self.save()
