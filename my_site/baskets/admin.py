from django.contrib import admin

from baskets.models import BasketAuth, BasketFK

# Register your models here.


@admin.register(BasketFK)
class BasketFKAdmin(admin.ModelAdmin):
    pass


@admin.register(BasketAuth)
class BasketAuthAdmin(admin.ModelAdmin):
    pass
