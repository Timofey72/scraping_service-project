from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages

from accounts.forms import UserUpdateForm, UserRegistrationForm, LoginUserForm
from accounts.models import MyUser


# class SignupUser(CreateView):
#     form_class = UserRegisterForm
#     template_name = 'accounts/signup.html'
#
#     def form_valid(self, form):
#         try:
#             user = MyUser.objects.create_user(email=self.request.POST['email'].lower(),
#                                               password=self.request.POST['password1'])
#             user.save()
#             messages.success(self.request, 'Успешная регистрация!')
#         except IntegrityError:
#             error = 'Пользователь с таким Email уже существует'
#             return render(self.request, 'accounts/signup.html', {'form': form, 'error': error})
#
#         login(self.request, user)
#         return redirect('index')

def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        try:
            new_user = form.save(commit=False)
            new_user.email = new_user.email.lower()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            messages.success(request, 'Пользователь добавлен в систему.')
            # return render(request, 'scraping/index.html', {'new_user': new_user})
            login(request, new_user)
            return redirect('index')
        except IntegrityError:
            messages.error(request, 'Пользователь с таким email уже существует!')
    else:
        messages.error(request, str(form.non_field_errors())[35: -10])
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    form = LoginUserForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email.lower(), password=password)
        login(request, user)
        messages.success(request, 'Успешный вход!')
        return redirect('index')
    else:
        messages.error(request, str(form.non_field_errors())[35: -10])
    return render(request, 'accounts/login.html', {'form': form})


# class LoginUser(LoginView):
#     authentication_form = UserLoginForm
#     template_name = 'accounts/login.html'


def logout_user(request):
    logout(request)
    return redirect('index')


@login_required
def update_user(request):
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user.city = data['city']
            user.language = data['language']
            user.send_email = data['send_email']
            user.save()
            messages.success(request, 'Данные успешно обновлены!')
    else:
        form = UserUpdateForm(initial={
            'city': user.city,
            'language': user.language,
            'send_email': user.send_email
        })
    return render(request, 'accounts/update.html', {'form': form})


@login_required
def delete_user(request):
    user = request.user
    if request.method == 'POST':
        qs = MyUser.objects.get(pk=user.pk)
        qs.delete()
        messages.error(request, 'Аккаунт пользователя успешно удалён!')
    return redirect('index')
