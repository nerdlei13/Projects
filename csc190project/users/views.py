from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def check_username(request):
    username = request.POST['username']
    user_check = User.objects.filter(username=username).first()
    if user_check is not None:
        return JsonResponse({"user_msg": user_check.username}, safe=False)
    else:
        return JsonResponse({"user_msg": ""}, safe=False)
        
     
@csrf_exempt
def check_email(request):
    email = request.POST['email']
    email_check = User.objects.filter(email=email).first()
    if email_check is not None:
        return JsonResponse({"email_msg": email_check.email}, safe=False)
    else:
        return JsonResponse({"email_msg": ""}, safe=False)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect('index')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('regular_search')
        else:
            messages.error(request, f'*Invalid password or username.')
            return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})
