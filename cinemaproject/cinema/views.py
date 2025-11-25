from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Movie, Session, Booking


def home(request):
    return render(request, 'cinema/home.html')


def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'cinema/movie_list.html', {'movies': movies})


def movie_detail(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    sessions = Session.objects.filter(movie=movie)
    return render(request, 'cinema/movie_detail.html', {
        'movie': movie,
        'sessions': sessions
    })


def session_list(request):
    sessions = Session.objects.all()
    return render(request, 'cinema/session_list.html', {'sessions': sessions})


@login_required
def booking(request, session_id):
    try:
        session = Session.objects.get(id=session_id)
        if request.method == 'POST':
            seats_count = int(request.POST.get('seats', 1))
            if seats_count <= 0:
                messages.error(request, 'Количество мест должно быть больше 0')
                return render(request, 'cinema/booking.html', {'session': session})

            total_price = session.price * seats_count
            Booking.objects.create(
                user=request.user,
                session=session,
                seats_count=seats_count,
                total_price=total_price,
                is_confirmed=True
            )
            messages.success(request, f'Бронь на {seats_count} мест успешно создана!')
            return redirect('home')

        return render(request, 'cinema/booking.html', {'session': session})

    except Session.DoesNotExist:
        messages.error(request, 'Сеанс не найден')
        return redirect('home')
