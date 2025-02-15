from django.shortcuts import render
from rest_framework import viewsets, pagination, filters

from rest_framework.permissions import IsAuthenticated
from products.permissions import IsOwnerOrReadOnly
from products.models import Category, Review, Order
from products.serializers import CategorySerializer, ReviewSerializer, OrderSerializer
# Create your views here.


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer





















