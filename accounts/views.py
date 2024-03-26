from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import get_user_model, login, logout, authenticate

User = get_user_model()


def sign_up(request):
    error_message = ''

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        username_exist = User.objects.filter(username=username).exists()
        email_exist = User.objects.filter(email=email).exists()

        if not (username_exist or email_exist):
            user = User.objects.create_user(username=username, password=password, email=email)
            login(request, user)
            return redirect(reverse('home'))
        elif username_exist and email_exist:
            error_message = f'Username "{username}" and email "{email}" already used!'
        elif username_exist:
            error_message = f'Username "{username}" already used!'
        else:
            error_message = f'Email "{email}" already used!'

    return render(request, 'accounts/sign-up.html', {"error": error_message})


def sign_in(request):
    error_message = ''

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect(reverse('home'))
        else:
            error_message = 'User account does not exist!'

    return render(request, 'accounts/sign-in.html', {'error': error_message})


@login_required
def sign_out(request):
    logout(request)
    return redirect(reverse('home'))
