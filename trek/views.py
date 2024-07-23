from rest_framework import generics, status,filters,permissions
from django_filters.rest_framework import DjangoFilterBackend
from core.utils.filters import TrekCountryCodeFilter
from .models import Trek, Itinerary,Inclusion,Gallery
from .serializers import TrekSerializer, ItinerarySerializer, InclusionSerializer,GallerySerializer
from core.utils.pagination import CustomPagination
from core.utils.response import PrepareResponse


class InclusionListCreateView(generics.ListCreateAPIView):
    queryset = Inclusion.objects.all()
    serializer_class = InclusionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        trek_id = request.query_params.get('trek_id')
        if trek_id:
            self.queryset = self.queryset.filter(trek_id=trek_id)
        serializer = self.get_serializer(self.queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Inclusions retrieved successfully",
            data=serializer.data
        )
        return response.send()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = PrepareResponse(
                success=True,
                message="Inclusion created successfully",
                data=serializer.data
            )
            return response.send(code=201)
        else:
            response = PrepareResponse(
                success=False,
                message="Inclusion creation failed",
                errors=serializer.errors
            )
            return response.send(code=400)
        
        
class GalleryListCreateView(generics.ListCreateAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        trek_id = request.query_params.get('trek_id')
        if trek_id:
            self.queryset = self.queryset.filter(trek_id=trek_id)
        serializer = self.get_serializer(self.queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Gallery retrieved successfully",
            data=serializer.data
        )
        return response.send()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = PrepareResponse(
                success=True,
                message="Gallery item created successfully",
                data=serializer.data
            )
            return response.send(code=201)
        else:
            response = PrepareResponse(
                success=False,
                message="Gallery item creation failed",
                errors=serializer.errors
            )
            return response.send(code=400)

class TrekListCreateView(generics.ListCreateAPIView):
    queryset = Trek.objects.all()
    serializer_class = TrekSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [TrekCountryCodeFilter, DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'location__name']
    ordering_fields = ['price_per_day', 'max_participants']


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Treks retrieved successfully",
            data=serializer.data
        )
        return response.send()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = PrepareResponse(
                success=True,
                message="Trek created successfully",
                data=serializer.data
            )
            return response.send(code=status.HTTP_201_CREATED)
        else:
            response = PrepareResponse(
                success=False,
                message="Trek creation failed",
                errors=serializer.errors
            )
            return response.send(code=status.HTTP_400_BAD_REQUEST)
class TrekDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trek.objects.all()
    serializer_class = TrekSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response = PrepareResponse(
            success=True,
            message="Trek retrieved successfully",
            data=serializer.data
        )
        return response.send()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            response = PrepareResponse(
                success=True,
                message="Trek updated successfully",
                data=serializer.data
            )
            return response.send()
        else:
            response = PrepareResponse(
                success=False,
                message="Trek update failed",
                errors=serializer.errors
            )
            return response.send(code=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        response = PrepareResponse(
            success=True,
            message="Trek deleted successfully"
        )
        return response.send()

class ItineraryListCreateView(generics.ListCreateAPIView):
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer

    def get_queryset(self):
        return self.queryset.filter(trek_id=self.kwargs['trek_id'])

    def create(self, request, *args, **kwargs):
        trek_id = kwargs['trek_id']
        data = request.data.copy()
        data['trek'] = trek_id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = PrepareResponse(
                success=True,
                message="Itinerary created successfully",
                data=serializer.data
            )
            return response.send(code=status.HTTP_201_CREATED)
        else:
            response = PrepareResponse(
                success=False,
                message="Itinerary creation failed",
                errors=serializer.errors
            )
            return response.send(code=status.HTTP_400_BAD_REQUEST)

class ItineraryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer

    def get_queryset(self):
        return self.queryset.filter(trek_id=self.kwargs['trek_id'])

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response = PrepareResponse(
            success=True,
            message="Itinerary retrieved successfully",
            data=serializer.data
        )
        return response.send()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            response = PrepareResponse(
                success=True,
                message="Itinerary updated successfully",
                data=serializer.data
            )
            return response.send()
        else:
            response = PrepareResponse(
                success=False,
                message="Itinerary update failed",
                errors=serializer.errors
            )
            return response.send(code=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        response = PrepareResponse(
            success=True,
            message="Itinerary deleted successfully"
        )
        return response.send()