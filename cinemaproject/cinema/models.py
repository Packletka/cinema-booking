from django.db import models
from django.contrib.auth.models import User


class CinemaHall(models.Model):
    """Модель кинозала"""
    name = models.CharField(max_length=100, verbose_name="Название зала")
    capacity = models.IntegerField(verbose_name="Вместимость")
    rows = models.IntegerField(verbose_name="Количество рядов")
    seats_per_row = models.IntegerField(verbose_name="Мест в ряду")

    def __str__(self):
        return f"{self.name} ({self.capacity} мест)"

    class Meta:
        verbose_name = "Кинозал"
        verbose_name_plural = "Кинозалы"


class Seat(models.Model):
    """Модель конкретного места в зале"""
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, verbose_name="Зал")
    row = models.IntegerField(verbose_name="Ряд")
    number = models.IntegerField(verbose_name="Номер места")

    def __str__(self):
        return f"Ряд {self.row}, Место {self.number}"

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"
        unique_together = ['hall', 'row', 'number']


class Movie(models.Model):
    """Модель фильма (оставляем как было)"""
    title = models.CharField(max_length=200, verbose_name="Название фильма")
    description = models.TextField(verbose_name="Описание")
    duration = models.IntegerField(verbose_name="Продолжительность (мин)")
    genre = models.CharField(max_length=100, verbose_name="Жанр")
    rating = models.FloatField(default=0.0, verbose_name="Рейтинг")
    poster = models.ImageField(upload_to='posters/', null=True, blank=True, verbose_name="Постер")
    trailer_url = models.URLField(blank=True, verbose_name="Трейлер")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class Session(models.Model):
    """Модель сеанса"""
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Фильм")
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, verbose_name="Зал")
    start_time = models.DateTimeField(verbose_name="Время начала")
    end_time = models.DateTimeField(verbose_name="Время окончания")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return f"{self.movie.title} - {self.start_time.strftime('%d.%m.%Y %H:%M')}"

    class Meta:
        verbose_name = "Сеанс"
        verbose_name_plural = "Сеансы"
        ordering = ['start_time']


class Booking(models.Model):
    """Модель бронирования"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name="Сеанс")
    seats = models.ManyToManyField(Seat, verbose_name="Забронированные места")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата бронирования")
    is_confirmed = models.BooleanField(default=True, verbose_name="Подтверждено")

    def __str__(self):
        seats_count = self.seats.count()
        return f"{self.user.username} - {self.session.movie.title} ({seats_count} мест)"

    class Meta:
        verbose_name = "Бронь"
        verbose_name_plural = "Брони"
