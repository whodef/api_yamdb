from django.db.models import Avg
from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from api.permisions import IsAdminSuperuserOrReadOnly

from categories.models import Category, Genre, Title
from api.filters import TitleFilter
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminSuperuserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',) 

    def perform_create(self, serializer):
        serializer.save()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminSuperuserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',) 

    def perform_create(self, serializer):
        serializer.save()


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    permission_classes = (IsAdminSuperuserOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TitleFilter
    search_fields = ('name',) 

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        return Title.objects.annotate(rating=Avg('reviews__rating')).order_by(
            'name'
        )
