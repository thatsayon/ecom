from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from django.db import IntegrityError

from authentication.authentication import APIKeyAuthentication
from subscriptions.permissions import HasValidSubscription
from .models import (
    Category,
    Product,
)
from .serializers import (
    CategorySerializer, 
    ProductSerializer
)

class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [HasValidSubscription]
    authentication_classes = [APIKeyAuthentication]

    def get_queryset(self):
        return Category.objects.filter(subscription=self.request.subscription)

    def perform_create(self, serializer):
        serializer.save(subscription=self.request.subscription)

class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [HasValidSubscription]
    authentication_classes = [APIKeyAuthentication]

    def get_queryset(self):
        return Product.objects.filter(subscription=self.request.subscription)

    def perform_create(self, serializer):
        try:
            serializer.save(subscription=self.request.subscription)
        except IntegrityError as e:
            if 'slug' in str(e):
                raise ValidationError({'slug': 'This slug already exists. Please choose a different one.'})
            raise ValidationError('A database error occurred.')
