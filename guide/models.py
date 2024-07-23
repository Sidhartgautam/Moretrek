from django.db import models
from trek.models import Trek

class Guide(models.Model):
    name= models.CharField(max_length=255)
    experience = models.CharField(max_length=255)


    def __str__(self):
        return self.name
    
class GuideRate(models.Model):
    guide =models.ForeignKey(Guide, on_delete=models.CASCADE,related_name='guide_rates')
    trek =models.ForeignKey(Trek, on_delete=models.CASCADE,related_name='guide_rates')
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('guide', 'trek')

    def __str__(self):
        return f"{self.guide.name} - {self.trek.name}-{self.daily_rate}"
    