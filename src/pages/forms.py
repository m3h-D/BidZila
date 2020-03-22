from django import forms


class ContactForm(forms.Form):
    first_name = forms.CharField(label="نام",
                                 required=False, max_length=100, help_text="حداکثر از 100 حرف می توانید استفاده کنید")
    last_name = forms.CharField(label='نام خانوادگی',
                                required=False, max_length=100, help_text="حداکثر از 100 حرف می توانید استفاده کنید")
    sender = forms.EmailField(label="ایمیل", required=True)
    subject = forms.CharField(label="موضوع", required=False, max_length=120)
    comment = forms.CharField(
        label="توضیحات", required=True, widget=forms.Textarea)
