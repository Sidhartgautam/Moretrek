from django.db import models
from users.models import UserProfile
from trek.models import Trek
from django.core.exceptions import ValidationError

class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews')
    trek = models.ForeignKey(Trek, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'trek')

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError('Rating must be between 1 and 5.')
        if self.comment and self.comment.strip() == "":
            raise ValidationError('Comment cannot be empty.')

    def __str__(self):
        return f'Review by {self.user.user.username} for {self.trek.name}'
