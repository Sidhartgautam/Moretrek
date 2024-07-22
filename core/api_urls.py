from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

#urls

     path ('users/', include('users.urls')),
    path ('trek/', include('trek.urls')),
    path ('location/', include('location.urls')),
    path ('booking/', include('booking.urls')),
    path ('review/', include('reviews.urls')),
]