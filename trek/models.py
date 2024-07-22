from django.db import models
from location.models import Location, Country
from django.core.exceptions import ValidationError


class Inclusion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    trek = models.ForeignKey('Trek', related_name='inclusions', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Exclusion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    trek = models.ForeignKey('Trek', related_name='exclusions', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Trek(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    max_participants = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='treks', null=True, blank=True)

    def clean(self):
        # Ensure price_per_day is positive
        if self.price_per_day <= 0:
            raise ValidationError('Price per day must be positive.')
        # Ensure max_participants is positive
        if self.max_participants <= 0:
            raise ValidationError('Max participants must be positive.')

    def __str__(self):
        return self.name

class Itinerary(models.Model):
    trek = models.ForeignKey(Trek, related_name='itineraries', on_delete=models.CASCADE)
    day = models.IntegerField()
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    from_location = models.CharField(max_length=100, null=True, blank=True)
    to_location = models.CharField(max_length=100,null=True, blank=True)
    from_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    from_lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    to_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    to_lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def clean(self):
        if self.day <= 0:
            raise ValidationError('Day must be positive.')
    

    def __str__(self):
        return f"Day {self.day} of {self.trek.name}"

class Gallery(models.Model):
    trek = models.ForeignKey(Trek, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/treks/gallery/')
    caption = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.caption if self.caption else 'Image'