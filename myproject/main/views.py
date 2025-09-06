from users.models import CustomUser
from .forms import CardForm
from .models import Card
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


@login_required
def profile_view(request, user_id):
    # Запрет для admin и analyst
    if request.user.role in ['admin', 'analyst']:
        return HttpResponseForbidden("У вас нет доступа к профилю")

    profile_user = get_object_or_404(CustomUser, id=user_id)
    cards = Card.objects.filter(user=profile_user).order_by('-created_at')

    return render(request, 'main/profile.html', {
        'profile_user': profile_user,
        'cards': cards,
    })

def home_view(request):
    cards = Card.objects.all().order_by('-created_at')

    return render(request, "main/home.html", {
        'cards': cards
    })

@login_required
def create_card_view(request):
    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            return redirect('home')
    else:
        form = CardForm()
    return render(request, 'main/create_card.html', {'form': form})

@login_required
def edit_card_view(request, card_id):
    card = get_object_or_404(Card, id=card_id, user=request.user)  # только владелец
    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CardForm(instance=card)
    return render(request, 'main/create_card.html', {'form': form, 'edit': True})

@login_required
def delete_card_view(request, card_id):
    card = get_object_or_404(Card, id=card_id, user=request.user)  # только владелец
    if request.method == 'POST':
        card.delete()
        return redirect('home')
    return render(request, 'main/delete_card.html', {'card': card})


@login_required
def admin_panel_view(request):
    # Можно потом наполнить контентом
    return render(request, 'main/admin_panel.html')

@login_required
def manager_panel_view(request):
    # Можно потом наполнить контентом
    return render(request, 'main/manager_panel.html')