from django.contrib import admin
from .models import Trek, Itinerary

class ItineraryInline(admin.TabularInline):
    model = Itinerary
    extra = 1

class TrekAdmin(admin.ModelAdmin):
    inlines = [ItineraryInline]
    list_display = ('name', 'location', 'price_per_day', 'max_participants')
    search_fields = ('name', 'location__name')
    list_filter = ('location',)

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)

admin.site.register(Trek, TrekAdmin)
