from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateFromToRangeFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Application
from .serializers import ApplicationSerializer

class ApplicationFilter(FilterSet):
    date_applied = DateFromToRangeFilter()
    
    class Meta:
        model = Application
        fields = {
            'company_name': ['icontains'],
            'job_title': ['icontains'],
            'position': ['icontains'],
            'status': ['exact'],
            'date_applied': ['exact', 'gte', 'lte'],
        }

class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ApplicationFilter
    search_fields = ['company_name', 'job_title', 'position', 'job_description']
    ordering_fields = ['company_name', 'date_applied', 'status']
    ordering = ['-date_applied']

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        print("Received data:", request.data)  # Debug log
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("Validation errors:", serializer.errors)  # Debug log
            return Response(
                {
                    "detail": "Validation failed",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Ensure users can only update their own applications
        if instance.user != request.user:
            return Response(
                {"error": "You don't have permission to update this application"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Ensure users can only delete their own applications
        if instance.user != request.user:
            return Response(
                {"error": "You don't have permission to delete this application"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs) 