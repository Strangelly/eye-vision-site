from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Full Name", "class": "form-control"}), required=True)
    shipping_email = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Email", "class": "form-control"}), required=True)
    shipping_address1 = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "address1", "class": "form-control"}), required=True)
    shipping_address2 = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "address2", "class": "form-control"}), required=False)
    shipping_city = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "city", "class": "form-control"}), required=True)
    shipping_country = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "country", "class": "form-control"}), required=True)
    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_country']

        exclude = ['user']