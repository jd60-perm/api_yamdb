from django.shortcuts import render
from rest_framework import filters, mixins, status, viewsets
from reviews import models
from . import serializers, permissions
from django_filters.rest_framework import DjangoFilterBackend


class CommentViewSet(viewsets.ModelViewSet):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = models.Title.objects.all()
    serializer_class = serializers.TitleSerializer
    permission_classes = (permissions.AdminOrGetMethod,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')


class GenreViewSet(
    mixins.DestroyModelMixin, mixins.ListModelMixin,
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = (permissions.AdminOrGetMethod,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(
    mixins.DestroyModelMixin, mixins.ListModelMixin,
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (permissions.AdminOrGetMethod,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
