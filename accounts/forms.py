from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(min_length=6, error_messages={'required': 'Введите пароль!'},
                               widget=forms.PasswordInput(attrs={
                                   'placeholder': 'Введите пароль'
                               }))
    confirm_password = forms.CharField(min_length=6, error_messages={'required': 'Подтвердите пароль!'},
                                       widget=forms.PasswordInput(attrs={
                                           'placeholder': 'Подтвердите пароль'
                                       }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'city', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите Email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Введите номер телефона'
        self.fields['city'].widget.attrs['placeholder'] = 'Введите город'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Пароли не совпадают!'
            )


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number', 'city', 'street')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
