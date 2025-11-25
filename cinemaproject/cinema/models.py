from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
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


class CinemaHall(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название зала")
    capacity = models.IntegerField(verbose_name="Вместимость")
    rows = models.IntegerField(verbose_name="Количество рядов")
    seats_per_row = models.IntegerField(verbose_name="Мест в ряду")

    def __str__(self):
        return f"{self.name} ({self.capacity} мест)"

    class Meta:
        verbose_name = "Кинозал"
        verbose_name_plural = "Кинозалы"


class Session(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Фильм")
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, verbose_name="Зал")
    start_time = models.DateTimeField(verbose_name="Время начала")
    end_time = models.DateTimeField(verbose_name="Время окончания")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return f"{self.movie.title} - {self.start_time}"

    class Meta:
        verbose_name = "Сеанс"
        verbose_name_plural = "Сеансы"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name="Сеанс")
    seats_count = models.IntegerField(verbose_name="Количество мест")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата бронирования")
    is_confirmed = models.BooleanField(default=False, verbose_name="Подтверждено")

    def __str__(self):
        return f"{self.user.username} - {self.session.movie.title}"

    class Meta:
        verbose_name = "Бронь"
        verbose_name_plural = "Брони"
