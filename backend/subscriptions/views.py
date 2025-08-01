from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.db import IntegrityError
from django.core.exceptions import ValidationError

from .models import Subscription, Plan
from .serializers import SubscriptionSerializer


class SubscriptionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Check if user already has a subscription
        if hasattr(user, 'subscription'):
            return Response({'error': 'Already subscribed'}, status=status.HTTP_400_BAD_REQUEST)

        plan_slug = request.data.get('plan')
        if not plan_slug:
            return Response({'error': 'Missing plan'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            plan = Plan.objects.get(slug=plan_slug)
        except Plan.DoesNotExist:
            return Response({'error': 'Invalid plan'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Creating subscription - use save() to ensure save() method logic runs
            subscription = Subscription(user=user, plan=plan)
            subscription.save()  # This will trigger the save() method logic
            serializer = SubscriptionSerializer(subscription)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Failed to create subscription'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RegenerateAPIKeyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Check if user already has a subscription
        if not hasattr(user, 'subscription'):
            return Response({'error': 'No subscription found'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Regenerate API key - use save() to ensure save() method logic runs
            user.subscription.rotate_key()
            serializer = SubscriptionSerializer(user.subscription)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Failed to regenerate API key'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)