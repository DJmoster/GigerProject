from django import forms

class ReviewForm(forms.Form):
    name    = forms.CharField(max_length=255)
    email   = forms.CharField(max_length=255)
    review  = forms.CharField(max_length=255)
    stars   = forms.IntegerField()


class OrderForm(forms.Form):
    name            = forms.CharField(max_length=255)
    surname         = forms.CharField(max_length=255)
    city            = forms.CharField(max_length=255)
    street          = forms.CharField(max_length=255)
    streetNumber    = forms.CharField(max_length=10)
    phoneNubmer     = forms.CharField(max_length=15)
    shipping_method = forms.CharField(max_length=255)
    products        = forms.CharField(max_length=255)