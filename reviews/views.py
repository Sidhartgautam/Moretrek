from rest_framework import generics, permissions, status
from .models import Review
from .serializers import ReviewSerializer
from core.utils.pagination import CustomPagination
from core.utils.response import PrepareResponse

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
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
            message="Reviews retrieved successfully",
            data=serializer.data
        )
        return response.send()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user.profile)
            response = PrepareResponse(
                success=True,
                message="Review created successfully",
                data=serializer.data
            )
            return response.send(code=status.HTTP_201_CREATED)
        else:
            response = PrepareResponse(
                success=False,
                message="Review creation failed",
                errors=serializer.errors
            )
            return response.send(code=status.HTTP_400_BAD_REQUEST)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user.profile)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response = PrepareResponse(
            success=True,
            message="Review retrieved successfully",
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
                message="Review updated successfully",
                data=serializer.data
            )
            return response.send()
        else:
            response = PrepareResponse(
                success=False,
                message="Review update failed",
                errors=serializer.errors
            )
            return response.send(code=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        response = PrepareResponse(
            success=True,
            message="Review deleted successfully"
        )
        return response.send()
