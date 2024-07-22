from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import UserProfile, User


User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name'
                  )

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": ("Email already exists")})
        return super().validate(data)
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError({"username": ("Username already exists")})
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError({"password": ("Password must be at least 8 characters")})
        return value
    
class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = ('id', 'username','email','bio','avatar','gender','date_of_birth','city','country','zip_code','state')
    def get_username(self, obj):
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email
    
class UserListSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email','profile')


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate (self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    msg = ("User account is disabled.")
                    raise serializers.ValidationError(msg)
            else:
                msg = ("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg)
        else:
            msg = ("Must include " "username and password.")
            raise serializers.ValidationError(msg)

        data["user"] = user
        return data
    