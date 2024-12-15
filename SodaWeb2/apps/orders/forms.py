from django import forms

class OrderForm(forms.Form):
    name = forms.CharField(label='Имя:', min_length=2, max_length=30, required=True)
    phone = forms.CharField(label='Номер телефона', min_length=10, max_length=11, required=False)
    tg_username = forms.CharField(label='Ник в Telegram', min_length=4, max_length=50, required=True)