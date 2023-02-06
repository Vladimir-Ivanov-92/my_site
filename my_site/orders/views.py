from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from orders.forms import OrderForm
from orders.models import Order
from products.utils import DataMixin


class OrderCreateView(DataMixin, CreateView):
    template_name = 'orders/order_create.html'
    form_class = OrderForm
    success_url = 'products_home'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title="Создание заказа")
        return dict(list(context.items()) + list(context_def.items()))

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.initiator = self.request.user
            super().form_valid(form)
            order = Order.objects.get(initiator=self.request.user)
            order.update_after_oder()
        else:
            form.instance.csrftoken = self.request.COOKIES['csrftoken']
            super().form_valid(form)
            csrftoken = self.request.COOKIES['csrftoken']
            order = Order.objects.get(csrftoken=csrftoken)
            order.update_after_oder(csrftoken=csrftoken)
        return HttpResponseRedirect(reverse_lazy('products_home'))
