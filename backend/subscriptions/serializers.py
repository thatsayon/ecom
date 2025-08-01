from rest_framework import serializers
from .models import Subscription, Plan

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = [
            'id', 'slug', 'name', 'description', 'api_quota', 'period_days'
        ]

class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = [
            'id', 'user', 'plan', 'api_key', 'is_active', 'usage_count', 'reset_at'
        ]