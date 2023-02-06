from baskets.models import BasketAuth, BasketFK
from django.http import HttpResponseRedirect
from products.models import Product


def basket_add(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    basket = BasketFK.objects.filter(csrftoken=request.COOKIES['csrftoken'], product=product)

    if not basket.exists():
        BasketFK.objects.create(csrftoken=request.COOKIES['csrftoken'], product=product, amount=1)
    else:
        basket = basket.first()
        basket.amount += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove(request, basket_id):
    basket = BasketFK.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_auth(request):
    baskets = BasketFK.objects.filter(csrftoken=request.COOKIES['csrftoken'])
    for basket in baskets:
        product = basket.product
        basket_add = BasketAuth.objects.filter(user=request.user, product=product)
        if not basket_add.exists():
            BasketAuth.objects.create(user=request.user, product=basket.product, amount=basket.amount,
                                      time_create=basket.time_create)
        else:
            basket_add = BasketAuth.objects.get(user=request.user, product=basket.product)
            basket_add.amount += 1
            basket_add.save()
        basket.delete()


def basket_add_auth(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    basket = BasketAuth.objects.filter(user=request.user, product=product)

    if not basket.exists():
        BasketAuth.objects.create(user=request.user, product=product, amount=1)
    else:
        basket = basket.first()
        basket.amount += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove_auth(request, basket_id):
    basket = BasketAuth.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
