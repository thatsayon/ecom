from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
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

    def get_queryset(self):
        return Product.objects.filter(subscription=self.request.subscription)

    def perform_create(self, serializer):
        serializer.save(subscription=self.request.subscription)
