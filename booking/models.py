from django.db import models
from users.models import UserProfile
from trek.models import Trek

class Booking(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='bookings')
    trek = models.ForeignKey(Trek, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    num_of_participants = models.IntegerField()

    def total_price(self):
        days = (self.end_date - self.start_date).days + 1  # Include the last day in the count
        return days * self.trek.price_per_day * self.num_of_participants

    def save(self, *args, **kwargs):
        self.total_price = self.total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.trek} - {self.start_date} - {self.end_date} - {self.num_of_participants}"
