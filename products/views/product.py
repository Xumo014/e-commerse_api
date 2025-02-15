from rest_framework import viewsets, filters, pagination
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models
from products.filters import ProductFilter
from django_filters import rest_framework as django_filters

from products.models import Product
from products.serializers import ProductSerializer
from products.permissions import *



class CustomPagination(pagination.PageNumberPagination):
    page_size = 10


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    pagination_class = CustomPagination

    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ProductFilter
    search_fields = ['name', 'description']


# Bitta categoriyaga tegishlilarni olish
    def list(self, request, *args, **kwargs):
        category = request.query_params.get('category', None)
        if category:
            self.queryset = self.queryset.filter(category=category)
        return super().list(request, *args, **kwargs)

# shu productga aloqador productlarni olish
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        related_products = Product.objects.filter(category=instance.category).exclude(id=instance.id)[:2]
        related_serializer = ProductSerializer(related_products, many=True)
        return Response({
            'products': serializer.data,
            'related_products': related_serializer.data
        })

#Eng ko'p reytingdagi mahsulotlarni olish
    @action(detail=False, methods=['get'])
    def top_rated(self, request):
        top_products = Product.objects.annotate(avg_rating=models.Avg('reviews__rating')).order_by('-avg_rating')[:2]
        serializer = ProductSerializer(top_products, many=True)
        return Response(serializer.data)

# Bitta mahsulotni reytingini olish
    @action(detail=True, methods=['get'])
    def average_rating(self):
        product = self.get_object()
        reviews = product.reviews.all()

        if reviews.count() == 0:
            return Response({'Average Rating': 0})

        avg_rating = sum([review.rating for review in reviews]) / reviews.count()

        return Response({'Average Rating': avg_rating})
