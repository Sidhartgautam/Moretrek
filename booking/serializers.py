from rest_framework import serializers
from .models import Booking
# from users.serializers import UserProfileSerializer

class BookingSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()
    user = serializers.UUIDField(read_only=True)

    class Meta:
        model = Booking
        fields = ('id','user', 'trek','start_date', 'end_date', 'num_of_participants', 'total_price')
    
    def validate(self, data):
        trek = data.get('trek')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        num_of_participants = data.get('num_of_participants')

        if start_date >= end_date:
            raise serializers.ValidationError("End date must be after start date.")

        if num_of_participants > trek.max_participants:
            raise serializers.ValidationError(f"Number of participants cannot exceed {trek.max_participants}.")
        return data