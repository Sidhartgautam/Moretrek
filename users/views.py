from rest_framework import status,generics,permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import User, UserProfile
from .serializers import UserRegisterSerializer, UserLoginSerializer,UserProfileSerializer
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken
from core.utils.response import PrepareResponse


class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Create a user profile if it doesn't exist
            if not UserProfile.objects.filter(user=user).exists():
                UserProfile.objects.create(user=user)
            response = PrepareResponse(
                success=True,
                message="User registered successfully",
                data=serializer.data
            )
            return response.send(code=status.HTTP_201_CREATED)
        else:
            response = PrepareResponse(
                success=False,
                message="User registration failed",
                data=serializer.errors
            )
            return response.send(400)
    
class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)

            refresh = RefreshToken.for_user(user)
            response = PrepareResponse(
                success=True,
                message="Login successful",
                data={
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': {
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    }
                }
            )
            return response.send()
        else:
            response = PrepareResponse(
                success=False,
                message="Login failed",
                data=serializer.errors
            )
            return response.send(400)
        
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return self.request.user.profile
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=self.request.user)
            return self.request.user.profile

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        response = PrepareResponse(
            success=True,
            message="Profile retrieved successfully",
            data=serializer.data
        )
        return response.send()

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            response = PrepareResponse(
                success=True,
                message="Profile updated successfully",
                data=serializer.data
            )
            return response.send()
        else:
            response = PrepareResponse(
                success=False,
                message="Profile update failed",
                data=serializer.errors
            )
            return response.send(400)