from rest_framework import serializers
from .models import Guide,GuideRate

class GuideRateSerializer(serializers.ModelSerializer):
    guide = serializers.StringRelatedField()
    trek = serializers.StringRelatedField()

    class Meta:
        model =GuideRate
        fields = ('id','guide','trek','daily_rate')


class GuideSeerializer(serializers.ModelSerializer):
    guide_rates=GuideRateSerializer(many=True, read_only=True)

    class Meta:
        model = Guide
        fields = ('id','name','experience','guide_rates')
        