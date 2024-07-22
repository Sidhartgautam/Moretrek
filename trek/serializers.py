from rest_framework import serializers
from .models import Trek, Itinerary,Inclusion,Gallery,Exclusion
from location.models import Location, Country
from location.serializers import LocationSerializer

class InclusionSerializer(serializers.ModelSerializer):
    trek_id = serializers.PrimaryKeyRelatedField(queryset=Trek.objects.all(), source='trek', write_only=True)
    trek = serializers.StringRelatedField(read_only=True)
    description = serializers.CharField(required = True)
    class Meta:
        model = Inclusion
        fields = ('id','name','description','trek_id','trek')

class ExclusionSerializer(serializers.ModelSerializer):
    trek_id = serializers.PrimaryKeyRelatedField(queryset=Trek.objects.all(), source='trek', write_only=True)
    trek = serializers.StringRelatedField(read_only=True)
    description = serializers.CharField(required = True)
    class Meta:
        model = Exclusion
        fields = ('id','name','description','trek_id','trek')
class ItinerarySerializer(serializers.ModelSerializer):
    # trek_id = serializers.PrimaryKeyRelatedField(queryset=Trek.objects.all(), source='trek', write_only=True)

    trek = serializers.StringRelatedField(read_only=True)
    from_location = serializers.CharField(write_only=True)
    to_location = serializers.CharField(write_only=True)
    from_lat = serializers.DecimalField(max_digits=9, decimal_places=6, write_only=True)
    from_lon = serializers.DecimalField(max_digits=9, decimal_places=6, write_only=True)
    to_lat = serializers.DecimalField(max_digits=9, decimal_places=6, write_only=True)
    to_lon = serializers.DecimalField(max_digits=9, decimal_places=6, write_only=True)
    class Meta:
        model = Itinerary
        fields = (
            'id', 
            'trek',
            # 'trek_id',
            'day',
            'title', 
            'description', 
            'from_location', 
            'to_location', 
            'from_lat', 
            'from_lon', 
            'to_lat', 
            'to_lon'
        )
    

    def validate_day(self, value):
        if value <= 0:
            raise serializers.ValidationError("Day must be positive.")
        return value
    def validate_latitude(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError("Latitude must be between -90 and 90.")
        return value

    def validate_longitude(self, value):
        if value < -180 or value > 180:
            raise serializers.ValidationError("Longitude must be between -180 and 180.")
        return value
    def validate(self, data):
        data['from_lat'] = self.validate_latitude(data.get('from_lat'))
        data['to_lat'] = self.validate_latitude(data.get('to_lat'))
        data['from_lon'] = self.validate_longitude(data.get('from_lon'))
        data['to_lon'] = self.validate_longitude(data.get('to_lon'))
        return data
    
class GallerySerializer(serializers.ModelSerializer):
    trek_id = serializers.PrimaryKeyRelatedField(queryset=Trek.objects.all(), source='trek', write_only=True)
    trek = serializers.StringRelatedField(read_only=True)
    caption = serializers.CharField(required = True)
    class Meta:
        model = Gallery
        fields = (
            'id', 
            'image',
            'caption',
            'trek_id',
            'trek'
        )

class TrekSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    inclusions = InclusionSerializer(many=True, read_only=True)
    itineraries = ItinerarySerializer(many=True, read_only=True)
    gallery = GallerySerializer(many=True, read_only=True)
    location_id = serializers.UUIDField(write_only=True)
    country_code = serializers.CharField(write_only=True)

    class Meta:
        model = Trek
        fields = (
            'id', 
            'name', 
            'description', 
            'price_per_day', 
            'max_participants', 
            'location_id', 
            'location', 
            'inclusions',
            'itineraries',
            'gallery',
            'country_code'
        )
        read_only_fields = ('location', 'itineraries','inclusions', 'gallery')

    def create(self, validated_data):
        location_id = validated_data.pop('location_id')
        country_code = validated_data.pop('country_code')
        location = Location.objects.get(id=location_id)
        country = Country.objects.get(code=country_code)
        trek = Trek.objects.create(location=location, country=country, **validated_data)
        return trek

    def update(self, instance, validated_data):
        location_id = validated_data.pop('location_id', None)
        country_code = validated_data.pop('country_code', None)

        if location_id:
            location = Location.objects.get(id=location_id)
            instance.location = location

        if country_code:
            country = Country.objects.get(code=country_code)
            instance.country = country

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price_per_day = validated_data.get('price_per_day', instance.price_per_day)
        instance.max_participants = validated_data.get('max_participants', instance.max_participants)
        instance.save()
        return instance

    def validate_price_per_day(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price per day must be positive.")
        return value

    def validate_max_participants(self, value):
        if value <= 0:
            raise serializers.ValidationError("Max participants must be positive.")
        return value
