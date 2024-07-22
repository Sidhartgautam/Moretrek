from django.db import models
import uuid
from django.core.exceptions import ValidationError
class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.name

class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        unique_together = ('country', 'name')

    def clean(self):
        if self.latitude < -90 or self.latitude > 90:
            raise ValidationError('Latitude must be between -90 and 90.')
        if self.longitude < -180 or self.longitude > 180:
            raise ValidationError('Longitude must be between -180 and 180.')

    def __str__(self):
        return f"{self.name}, {self.country.name}"
