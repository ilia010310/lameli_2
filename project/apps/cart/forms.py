from django import forms
 


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(label='Количество', max_value=9999, initial=1)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)

