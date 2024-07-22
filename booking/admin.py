from django.contrib import admin
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'trek', 'start_date', 'end_date', 'num_of_participants', 'total_price')
    search_fields = ('user__user__username', 'trek__name')
    list_filter = ('start_date', 'end_date', 'trek')

admin.site.register(Booking, BookingAdmin)
