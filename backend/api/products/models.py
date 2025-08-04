from django.db import models
from subscriptions.models import Subscription
import uuid

class Category(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Product(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    
