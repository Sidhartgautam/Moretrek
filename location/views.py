from rest_framework import generics
from .models import Country, Location
from .serializers import CountrySerializer, LocationSerializer
from core.utils.pagination import CustomPagination
from core.utils.response import PrepareResponse

class CountryListView(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Countries retrieved successfully",
            data=serializer.data
        )
        return response.send()

class LocationListView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Locations retrieved successfully",
            data=serializer.data
        )
        return response.send()
