from django import template

from baskets.models import BasketAuth, BasketFK

register = template.Library()


@register.simple_tag()
def get_BasketFk_product_amount(request, pk):
    x = BasketFK.objects.get(csrftoken=request.COOKIES['csrftoken'], product_id=pk)
    return x.amount


@register.simple_tag()
def get_BasketAuth_product_amount(request, pk):
    x = BasketAuth.objects.get(user=request.user, product_id=pk)
    return x.amount
