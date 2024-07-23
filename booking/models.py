from django.db import models
from users.models import UserProfile
from trek.models import Trek
from guide.models import Guide, GuideRate

class Booking(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='bookings')
    trek = models.ForeignKey(Trek, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    num_of_participants = models.IntegerField()
    include_guide = models.BooleanField(default=False)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def save(self,*args, **kwargs):
        days=(self.end_date - self.start_date).days + 1  # Include the last day in the count
        trek_cost = self.trek.price_per_day * days* self.num_of_participants
        guide_cost = 0
        if self.include_guide and self.guide:
            guide_rate = GuideRate.objects.get(guide=self.guide, trek=self.trek)
            guide_cost = guide_rate.daily_rate * days
        self.total_price = trek_cost + guide_cost
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.user} - {self.trek} - {self.start_date} - {self.end_date} - {self.num_of_participants}"
