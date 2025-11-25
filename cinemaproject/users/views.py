from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.apps import apps
from django.utils import timezone
import datetime


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
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')

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


@login_required
def cancel_booking(request, booking_id):
    """Отмена бронирования"""
    Booking = apps.get_model('cinema', 'Booking')

    # Получаем бронь или возвращаем 404
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Проверяем, можно ли отменить бронь (например, не позже чем за 1 час до сеанса)
    can_cancel = True
    cancellation_message = ""

    if booking.session.start_time <= timezone.now() + datetime.timedelta(hours=1):
        can_cancel = False
        cancellation_message = "Невозможно отменить бронь менее чем за 1 час до сеанса"

    if request.method == 'POST' and can_cancel:
        # Удаляем бронь
        booking.delete()
        messages.success(request, 'Бронь успешно отменена!')
        return redirect('profile')
    elif request.method == 'POST' and not can_cancel:
        messages.error(request, cancellation_message)
        return redirect('profile')

    # Если GET-запрос, показываем страницу подтверждения
    context = {
        'booking': booking,
        'can_cancel': can_cancel,
        'cancellation_message': cancellation_message
    }
    return render(request, 'users/cancel_booking.html', context)
