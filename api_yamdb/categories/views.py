from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, filters, status, viewsets
from rest_framework.response import Response

from api.permissions import IsAdminSuperuserOrReadOnly
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
    lookup_field = 'slug'
    permission_classes = (IsAdminSuperuserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    
    def exist_validation(self, request):
        instance = Category.objects.filter(slug=self.kwargs.get('slug'))
        if not instance.exists():
            raise exceptions.MethodNotAllowed(method=request.method)

    def perform_create(self, serializer):
        serializer.save()

    def retrieve(self, request, *args, **kwargs):
        self.exist_validation(request)
        return super().retrieve(request,*args,**kwargs)

    def partial_update(self, request, *args, **kwargs):
        self.exist_validation(request)
        return super().partial_update(request, *args, **kwargs)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminSuperuserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def exist_validation(self, request):
        instance = Genre.objects.filter(slug=self.kwargs.get('slug'))
        if not instance.exists():
            raise exceptions.MethodNotAllowed(method=request.method)

    def perform_create(self, serializer):
        serializer.save()

    def retrieve(self, request, *args, **kwargs):
        self.exist_validation(request)
        return super().retrieve(request,*args,**kwargs)

    def partial_update(self, request, *args, **kwargs):
        self.exist_validation(request)
        return super().partial_update(request, *args, **kwargs)


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    permission_classes = (IsAdminSuperuserOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TitleFilter
    search_fields = ('name',)

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        return Title.objects.annotate(
            rating=Avg('reviews__rating')).order_by('name')
