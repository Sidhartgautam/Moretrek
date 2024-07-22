from django.urls import path
from .views import (
    TrekListCreateView,
      TrekDetailView,
        ItineraryListCreateView,
          ItineraryDetailView,
          InclusionListCreateView,
          ExclusionListCreateView,
          GalleryListCreateView)

urlpatterns = [
    path('treks/', TrekListCreateView.as_view(), name='trek-list-create'),
    path('treks/<int:pk>/', TrekDetailView.as_view(), name='trek-detail'),
    path('treks/<int:trek_id>/itineraries/', ItineraryListCreateView.as_view(), name='itinerary-list-create'),
    path('treks/<int:trek_id>/itineraries/<int:pk>/', ItineraryDetailView.as_view(), name='itinerary-detail'),
     path('inclusions/', InclusionListCreateView.as_view(), name='inclusion-list-create'),
    path('gallery/', GalleryListCreateView.as_view(), name='gallery-list-create'),  
    path('exclusions/', ExclusionListCreateView.as_view(), name='exclusion-list-create'),
]
