from django.db import models 
from subscriptions.models import Subscription
import uuid
import ulid

def generate_ulid():
    return str(ulid.new())

class Order(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    order_number = models.CharField(
        max_length=26, 
        unique=True, 
        default=generate_ulid,
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order ID: {self.order_number}"
