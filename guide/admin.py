from django.contrib import admin
from .models import Guide, GuideRate

@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ('name', 'experience')

@admin.register(GuideRate)
class GuideRateAdmin(admin.ModelAdmin):
    list_display = ('guide', 'trek', 'daily_rate')