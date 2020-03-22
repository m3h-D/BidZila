from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 10)]


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        label='تعداد', min_value=1, max_value=20, initial=1, widget=forms.HiddenInput)
    update = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput)


class CartAddBidForm(forms.Form):
    quantity = forms.IntegerField(
        label='تعداد', min_value=1, max_value=20, initial=1)
    update = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput)
