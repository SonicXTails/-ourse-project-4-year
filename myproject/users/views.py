from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.shortcuts import render, get_object_or_404
from .models import CustomUser


# Профиль пользователя
def profile_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    return render(request, 'users/profile.html', {
        'profile_user': user,
    })


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )
            if user:
                login(request, user)
                return redirect('/')
    else:
        form = CustomAuthenticationForm()
    return render(request, "users/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('/')
