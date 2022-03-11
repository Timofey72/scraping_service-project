from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

from accounts.models import MyUser
from scraping.models import City, Language


# class UserLoginForm(forms.Form):
#     email = forms.CharField(widget=forms.EmailField())
#     password = forms.CharField(widget=forms.PasswordInput())
#
#     def clean(self, *args, **kwargs):
#         email = self.cleaned_data.get('email')
#         password = self.cleaned_data.get('password')
#
#         if email and password:
#             qs = MyUser.objects.filter(email=email)
#         if not qs.exsits():
#             raise ValidationError('Такого пользователя не существует!')
#         if not check_password(password, qs.password):
#             raise ValidationError('Пароль не подходит. Попробуйте ещё раз!')
#         user = authenticate(email=email.lower(), password=password)
#         if not user:
#             raise ValidationError('Данный аккаунт отключён!')
#         return super(UserLoginForm, self).clean(*args, **kwargs)
#
#
# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField(label='Email')
#     password1 = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
#     password2 = forms.CharField(widget=forms.PasswordInput(), label='Повторите пароль')
#
#     class Meta:
#         model = MyUser
#         fields = ('email',)


class UserUpdateForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(), label='Город',
        to_field_name='slug', required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(), label='Специальность',
        to_field_name='slug', required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    send_email = forms.BooleanField(required=False, widget=forms.CheckboxInput(), label='Получать рассылку?')

    class Meta:
        model = MyUser
        fields = ('city', 'language', 'send_email')


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='Введите email',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Введите пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Введите пароль ещё раз',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = MyUser
        fields = ('email',)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email').strip().lower()
        password = self.cleaned_data.get('password').strip()
        password2 = self.cleaned_data.get('password2').strip()

        if email and password:
            qs = MyUser.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError('Пользователь с таким email уже существует!')
            if password != password2:
                raise forms.ValidationError('Пароли не совпадают!')
        return super(UserRegistrationForm, self).clean(*args, **kwargs)


class LoginUserForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email').strip().lower()
        password = self.cleaned_data.get('password').strip()

        if email and password:
            qs = MyUser.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError('Такого пользователя нет!')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Пароль не верный!')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Данный аккаунт отключен')
        return super(LoginUserForm, self).clean(*args, **kwargs)
