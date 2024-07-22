from django.contrib import admin
from .models import Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'trek', 'rating', 'comment', 'created_at')
    search_fields = ('user__user__username', 'trek__name')
    list_filter = ('rating', 'created_at')

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)

admin.site.register(Review, ReviewAdmin)
