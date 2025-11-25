from django.contrib import admin
from .models import Movie, CinemaHall, Session, Booking


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'rating', 'duration']
    list_filter = ['genre', 'rating']
    search_fields = ['title']


@admin.register(CinemaHall)
class CinemaHallAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity', 'rows', 'seats_per_row']


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['movie', 'hall', 'start_time', 'end_time', 'price']
    list_filter = ['start_time', 'hall']
    date_hierarchy = 'start_time'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'session', 'seats_count', 'total_price', 'created_at', 'is_confirmed']
    list_filter = ['created_at', 'is_confirmed']
