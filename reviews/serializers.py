from rest_framework import serializers
from .models import Review
from users.models import UserProfile

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Display only the user ID

    class Meta:
        model = Review
        fields = ('id', 'user', 'trek', 'rating', 'comment', 'created_at')

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate_comment(self, value):
        if value and value.strip() == "":
            raise serializers.ValidationError("Comment cannot be empty.")
        return value

    def validate(self, data):
        request = self.context.get('request')
        trek = data.get('trek')
        user_profile = request.user.profile

        if Review.objects.filter(user=user_profile, trek=trek).exists():
            raise serializers.ValidationError("You have already reviewed this trek.")

        return data
