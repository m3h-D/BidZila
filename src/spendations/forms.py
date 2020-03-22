from django import forms


class SpendForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1, max_value=1, initial=1, widget=forms.HiddenInput)
    update = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput)
