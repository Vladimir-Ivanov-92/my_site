from baskets.models import BasketAuth, BasketFK
from django.contrib import admin

# Register your models here.


@admin.register(BasketFK)
class BasketFKAdmin(admin.ModelAdmin):
    pass


@admin.register(BasketAuth)
class BasketAuthAdmin(admin.ModelAdmin):
    pass
