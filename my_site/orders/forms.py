from django import forms
from orders.models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(label="Имя", widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Вася'
        }
    ))
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Пупкин'
        }
    ))
    email = forms.EmailField(label="Адрес электронной почты", widget=forms.EmailInput(
        {'class': 'form-control',
         'placeholder': 'vasya@example.ru'
         }
    ))
    address = forms.CharField(label="Адрес доставки", widget=forms.TextInput(
        {'class': 'form-control',
         'placeholder': 'г. Мурманск, ул. Ленина д.1'
         }
    ))

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address']
