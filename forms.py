from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProductFilterForm(forms.Form):
    min_price = forms.DecimalField(label='Preț minim', required=False)
    max_price = forms.DecimalField(label='Preț maxim', required=False)
    min_stock = forms.IntegerField(label='Stoc minim', required=False)
    max_stock = forms.IntegerField(label='Stoc maxim', required=False)
    supplier = forms.CharField(label='Furnizor', required=False)
    delivery_method = forms.CharField(label='Modalitate de livrare', required=False)