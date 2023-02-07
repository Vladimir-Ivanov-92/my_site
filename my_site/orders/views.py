from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

from orders.forms import OrderForm
from orders.models import Order
from products.utils import DataMixin


class OrderCreateView(DataMixin, CreateView):
    template_name = 'orders/order_create.html'
    form_class = OrderForm
    success_url = 'order_is_create'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title="Создание заказа")
        return dict(list(context.items()) + list(context_def.items()))

    def get_initial(self):
        if self.request.user.is_authenticated:
            return {'email': self.request.user.email}
        else:
            return super().get_initial()

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.initiator = self.request.user
            form.instance.phone_number = form.cleaned_data['phone_number']
            if self.request.user.is_verified_email:
                super().form_valid(form)
            else:
                form.add_error('email', ValidationError('Электронная почта не подтверждена'))
                return super().form_invalid(form)
            order = Order.objects.get(initiator=self.request.user, status=0)
            order.update_after_oder()
            order.send_message_for_staff_about_order()
            if order.initiator.is_verified_email and (form.cleaned_data['email'] == order.initiator.email):
                order.send_message_for_user_about_order()
        else:
            form.instance.csrftoken = self.request.COOKIES['csrftoken']
            form.instance.phone_number = form.cleaned_data['phone_number']
            super().form_valid(form)
            csrftoken = self.request.COOKIES['csrftoken']
            order = Order.objects.get(csrftoken=csrftoken, status=0)
            order.update_after_oder(csrftoken=csrftoken)
            order.send_message_for_staff_about_order()
        return HttpResponseRedirect(reverse_lazy('order_is_create', args=[order.pk]))


class OrdersListView(DataMixin, ListView):
    template_name = 'orders/orders.html'
    queryset = Order.objects.all()
    ordering = ('-created')

    def get_context_data(self, *, object_list=None, **kwargs):  # FIXMI! Сделать ТitleMixin
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title="Заказы")
        return dict(list(context.items()) + list(context_def.items()))

    def get_queryset(self):
        queryset = super(OrdersListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(DataMixin, DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title=f"Заказ №{self.object.id}")
        return dict(list(context.items()) + list(context_def.items()))


class OrderIsCreateView(DataMixin, DetailView):
    template_name = 'orders/order_is_create.html'
    model = Order

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title=f"Создан заказ №{self.object.id}")
        return dict(list(context.items()) + list(context_def.items()))


class OrdersListForStaffView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'orders/orders_for_staff.html'
    model = Order
    ordering = ('status', '-created')
    paginate_by = 12

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy('products_home'))

    def get_context_data(self, *, object_list=None, **kwargs):  # FIXMI! Сделать ТitleMixin
        context = super().get_context_data(**kwargs)
        context['title'] = "Заказы"
        return context


def change_status_order(request, orders_id, status):
    order = Order.objects.filter(id=orders_id)
    order.update(status=status)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
