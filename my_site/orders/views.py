from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from orders.forms import OrderForm
from products.utils import DataMixin


class OrderCreateView(DataMixin, CreateView):
    template_name = 'orders/order_create.html'
    form_class = OrderForm
    success_url = reverse_lazy('order_create')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title="Создание заказа")
        return dict(list(context.items()) + list(context_def.items()))

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)
