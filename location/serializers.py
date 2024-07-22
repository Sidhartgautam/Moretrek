from rest_framework import serializers
from .models import Country, Location

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name', 'code')

    def validate_name(self, value):
        if Country.objects.filter(name=value).exists():
            raise serializers.ValidationError("Country name must be unique.")
        return value

    def validate_code(self, value):
        if Country.objects.filter(code=value).exists():
            raise serializers.ValidationError("Country code must be unique.")
        return value

class LocationSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    country_code = serializers.CharField(write_only=True)

    class Meta:
        model = Location
        fields = ('id', 'country', 'country_code', 'name', 'latitude', 'longitude')

    def create(self, validated_data):
        country_code = validated_data.pop('country_code')
        try:
            country = Country.objects.get(code=country_code)
        except Country.DoesNotExist:
            raise serializers.ValidationError("Country with this code does not exist.")
        location = Location.objects.create(country=country, **validated_data)
        return location

    def update(self, instance, validated_data):
        country_code = validated_data.pop('country_code', None)
        if country_code:
            try:
                country = Country.objects.get(code=country_code)
                instance.country = country
            except Country.DoesNotExist:
                raise serializers.ValidationError("Country with this code does not exist.")
        instance.name = validated_data.get('name', instance.name)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.save()
        return instance

    def validate_latitude(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError("Latitude must be between -90 and 90.")
        return value

    def validate_longitude(self, value):
        if value < -180 or value > 180:
            raise serializers.ValidationError("Longitude must be between -180 and 180.")
        return value

    def validate(self, data):
        country_code = data.get('country_code')
        name = data.get('name')
        try:
            country = Country.objects.get(code=country_code)
        except Country.DoesNotExist:
            raise serializers.ValidationError("Country with this code does not exist.")
        if Location.objects.filter(country=country, name=name).exists():
            raise serializers.ValidationError("Location name must be unique within the same country.")
        return data
