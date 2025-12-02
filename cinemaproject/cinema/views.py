from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Movie, Session, Booking, Seat, CinemaHall
from django.db.models import Q
from collections import defaultdict


def home(request):
    """Главная страница"""
    movies = Movie.objects.all()[:4]
    now = timezone.now()
    sessions = Session.objects.filter(start_time__gte=now).order_by('start_time')[:3]

    return render(request, 'cinema/home.html', {
        'movies': movies,
        'sessions': sessions
    })


def movie_list(request):
    """Список всех фильмов"""
    movies = Movie.objects.all()
    return render(request, 'cinema/movie_list.html', {'movies': movies})


def movie_detail(request, movie_id):
    """Детали фильма"""
    movie = get_object_or_404(Movie, id=movie_id)
    sessions = Session.objects.filter(movie=movie, start_time__gte=timezone.now())

    return render(request, 'cinema/movie_detail.html', {
        'movie': movie,
        'sessions': sessions
    })


def session_list(request):
    """Список всех сеансов"""
    sessions = Session.objects.filter(start_time__gte=timezone.now()).order_by('start_time')
    return render(request, 'cinema/session_list.html', {'sessions': sessions})


@login_required
def booking(request, session_id):
    """Бронирование мест для конкретного сеанса"""
    session = get_object_or_404(Session, id=session_id)
    hall = session.hall

    print(f"=== DEBUG: Бронирование для сеанса {session_id} ===")
    print(f"Зал: {hall.name}, ID зала: {hall.id}")

    # Получаем все места в зале
    all_seats = Seat.objects.filter(hall=hall).order_by('row', 'number')
    print(f"Всего мест в зале: {all_seats.count()}")
    print(f"ID мест в зале: {list(all_seats.values_list('id', flat=True))}")

    # Получаем занятые места на этот сеанс
    booked_seats_ids = Booking.objects.filter(
        session=session,
        is_confirmed=True
    ).values_list('seats__id', flat=True)

    print(f"Занятые ID мест: {list(booked_seats_ids)}")

    # Группируем места по рядам для отображения
    seats_by_row = defaultdict(list)
    for seat in all_seats:
        seats_by_row[seat.row].append({
            'id': seat.id,
            'number': seat.number,
            'is_booked': seat.id in booked_seats_ids
        })

    sorted_rows = sorted(seats_by_row.keys())

    if request.method == 'POST':
        print(f"=== DEBUG: POST запрос ===")
        print(f"POST данные: {request.POST}")

        # Получаем выбранные места
        selected_seat_ids = request.POST.getlist('seats')
        print(f"Выбранные ID мест: {selected_seat_ids}")

        if not selected_seat_ids:
            messages.error(request, 'Пожалуйста, выберите хотя бы одно место')
        else:
            # Проверяем, что выбранные места свободны
            available_seats = []
            for seat_id in selected_seat_ids:
                try:
                    seat = Seat.objects.get(id=seat_id)
                    print(f"Найдено место: ID={seat.id}, Ряд={seat.row}, Место={seat.number}")

                    if seat.id in booked_seats_ids:
                        messages.error(request, f'Место Ряд {seat.row}, Место {seat.number} уже занято')
                        return redirect('booking', session_id=session_id)

                    # Проверяем, что место из правильного зала
                    if seat.hall.id != hall.id:
                        messages.error(request, f'Место не принадлежит этому залу')
                        return redirect('booking', session_id=session_id)

                    available_seats.append(seat)

                except Seat.DoesNotExist:
                    print(f"ОШИБКА: Место с ID {seat_id} не найдено в базе!")
                    messages.error(request, f'Ошибка: место с ID {seat_id} не найдено. Обновите страницу.')
                    return redirect('booking', session_id=session_id)

            # Создаем бронь
            total_price = session.price * len(available_seats)
            booking_obj = Booking.objects.create(
                user=request.user,
                session=session,
                total_price=total_price
            )
            booking_obj.seats.set(available_seats)

            messages.success(request, f'Бронь на {len(available_seats)} мест успешно создана!')
            return redirect('profile')

    context = {
        'session': session,
        'hall': hall,
        'seats_by_row': dict(seats_by_row),
        'rows': sorted_rows,
        'price': session.price
    }

    return render(request, 'cinema/booking.html', context)
