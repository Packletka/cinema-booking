from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
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
    """Профиль пользователя с историей бронирований"""
    Booking = apps.get_model('cinema', 'Booking')

    # Получаем бронирования пользователя
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')

    # Считаем статистику
    total_bookings = bookings.count()
    confirmed_bookings = bookings.filter(is_confirmed=True).count()

    # Считаем общее количество билетов
    total_tickets = 0
    for booking in bookings:
        total_tickets += booking.seats.count()

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

    # Проверяем возможность отмены (не позже чем за 2 часа до сеанса)
    from django.utils import timezone
    import datetime

    can_cancel = True
    cancellation_message = ""

    time_until_session = booking.session.start_time - timezone.now()
    if time_until_session <= datetime.timedelta(hours=2):
        can_cancel = False
        cancellation_message = "Невозможно отменить бронь менее чем за 2 часа до сеанса"

    if request.method == 'POST' and can_cancel:
        # Получаем информацию о местах перед удалением
        seats_info = ", ".join([f"Ряд {seat.row}, Место {seat.number}" for seat in booking.seats.all()])
        seats_count = booking.seats.count()

        # Удаляем бронь
        booking.delete()
        messages.success(request, f'Бронь на {seats_count} мест ({seats_info}) успешно отменена!')
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
