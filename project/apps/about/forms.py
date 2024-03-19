from django import forms
from django_recaptcha.fields import ReCaptchaField
from apps.about.models import CallBack


class CallBackForm(forms.ModelForm):
    recaptcha = ReCaptchaField()
    name = forms.CharField(required=True,
                    widget=forms.TextInput(attrs={"class": "form-control",
                                                  'placeholder': 'Контактное лицо',
                                                  'style': 'width: 300px;'}))
    number = forms.CharField(required=True,
                                        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Телефон',
                                                                      'style': 'width: 300px;'}))

    class Meta:
        model = CallBack
        fields = ['number', 'name']
