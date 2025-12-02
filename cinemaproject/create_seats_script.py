import os
import django

# Настройка Django окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinemaproject.settings')
django.setup()

from cinema.models import CinemaHall, Seat


def create_seats():
    halls = CinemaHall.objects.all()

    if not halls.exists():
        print("Нет залов в базе данных. Сначала создайте залы через админку.")
        return

    total_created = 0

    for hall in halls:
        print(f"Создаем места для зала: {hall.name}")

        # Удаляем старые места если есть
        deleted_count, _ = Seat.objects.filter(hall=hall).delete()
        if deleted_count:
            print(f"Удалено {deleted_count} старых мест для зала '{hall.name}'")

        seats_created = 0
        for row in range(1, hall.rows + 1):
            for seat_num in range(1, hall.seats_per_row + 1):
                Seat.objects.create(
                    hall=hall,
                    row=row,
                    number=seat_num
                )
                seats_created += 1

        total_created += seats_created
        print(f"✓ Создано {seats_created} мест для зала '{hall.name}'")

    print(f"✅ Всего создано {total_created} мест во всех залах")


if __name__ == "__main__":
    create_seats()
