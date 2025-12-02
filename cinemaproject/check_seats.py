import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinemaproject.settings')
django.setup()

from cinema.models import CinemaHall, Seat, Session


def check_seats():
    print("=== ПРОВЕРКА МЕСТ В БАЗЕ ===")

    halls = CinemaHall.objects.all()
    for hall in halls:
        print(f"\nЗал: {hall.name} (ID: {hall.id})")
        seats = Seat.objects.filter(hall=hall)
        print(f"Количество мест: {seats.count()}")

        if seats.exists():
            print("Первые 10 мест:")
            for seat in seats[:10]:
                print(f"  ID: {seat.id}, Ряд: {seat.row}, Место: {seat.number}")

    print("\n=== СЕАНСЫ ===")
    sessions = Session.objects.all()
    for session in sessions:
        print(f"Сеанс {session.id}: {session.movie.title} в зале {session.hall.name}")


if __name__ == "__main__":
    check_seats()
