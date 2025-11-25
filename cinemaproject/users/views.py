from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

# Импорт через get_model для избежания циклических импортов
from django.apps import apps


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    # Получаем модель Booking динамически
    Booking = apps.get_model('cinema', 'Booking')

    # Получаем бронирования пользователя
    bookings = Booking.objects.filter(user=request.user)

    # Считаем статистику
    total_bookings = bookings.count()
    confirmed_bookings = bookings.filter(is_confirmed=True).count()
    total_tickets = bookings.aggregate(total=Sum('seats_count'))['total'] or 0

    context = {
        'bookings': bookings,
        'total_bookings': total_bookings,
        'confirmed_bookings': confirmed_bookings,
        'total_tickets': total_tickets,
    }
    return render(request, 'users/profile.html', context)