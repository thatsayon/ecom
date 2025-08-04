from rest_framework import generics
from .models import (
    Order
)
from .serializers import (
    OrderSerializer
)

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(subscription=self.request.subscription)

    def perform_create(self, serializer):
        serializer.save(subscription=self.request.subscription)
