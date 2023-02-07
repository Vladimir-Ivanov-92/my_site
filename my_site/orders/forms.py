from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import RegionalPhoneNumberWidget

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
        attrs={
            'class': 'form-control',
            'placeholder': 'vasya@example.ru'
         }
    ))
    phone_number = PhoneNumberField(label="Номер телефона", widget=RegionalPhoneNumberWidget(
        region='RU',
        attrs={
            'class': 'form-control',
            'placeholder': '+7(999)999-99-99',
        }
    ))
    address = forms.CharField(label="Адрес доставки", widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'г. Мурманск, ул. Ленина д.1'
         }
    ))

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address']
