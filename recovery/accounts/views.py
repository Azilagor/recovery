import random
import string
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PasswordResetForm

def generate_password(length=8):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

def password_reset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            login = form.login['login']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            new_password = generate_password()
            messages.success(request, f"Новый пароль для {email}: {new_password}")
            return redirect('password_reset')
    else:
        form = PasswordResetForm()
    return render(request, 'accounts/password_reset_form.html', {'form': form})
