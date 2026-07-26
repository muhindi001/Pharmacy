from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):

    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    queryset = Category.objects.filter(
        is_deleted=False
    )

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "category_name",
        "description",
    ]

    filterset_fields = [
        "is_active",
    ]

    ordering_fields = [
        "category_name",
        "created_at",
        "updated_at",
    ]

    ordering = [
        "category_name",
    ]

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()