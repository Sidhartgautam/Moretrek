from django.urls import path
from .views import CountryListView, LocationListView

urlpatterns = [
    path('countries/', CountryListView.as_view(), name='country-list'),
    path('locations/', LocationListView.as_view(), name='location-list'),
]
