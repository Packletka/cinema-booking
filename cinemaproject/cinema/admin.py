from django.contrib import admin
from .models import Movie, CinemaHall, Session, Booking, Seat


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['hall', 'row', 'number']
    list_filter = ['hall']
    search_fields = ['hall__name']


@admin.register(CinemaHall)
class CinemaHallAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity', 'rows', 'seats_per_row']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'rating', 'duration']
    list_filter = ['genre', 'rating']
    search_fields = ['title']


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['movie', 'hall', 'start_time', 'end_time', 'price']
    list_filter = ['start_time', 'hall']
    date_hierarchy = 'start_time'
    search_fields = ['movie__title']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'session', 'get_seats_count', 'total_price', 'created_at', 'is_confirmed']
    list_filter = ['created_at', 'is_confirmed', 'session']
    search_fields = ['user__username', 'session__movie__title']

    def get_seats_count(self, obj):
        return obj.seats.count()

    get_seats_count.short_description = 'Количество мест'
    get_seats_count.admin_order_field = 'seats__count'  # Для сортировки
