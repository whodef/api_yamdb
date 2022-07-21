from django.db.models import Avg
from rest_framework import viewsets

from categories.models import Category, Genre, Title
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def perform_create(self, serializer):
        serializer.save()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def perform_create(self, serializer):
        serializer.save()


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer 

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        return Title.objects.annotate(
            rating=Avg('reviews__rating')
        ).order_by('name')
        