# # authentication/authentication.py
# from rest_framework.authentication import BaseAuthentication
# from rest_framework.exceptions     import AuthenticationFailed
# from subscriptions.models         import Subscription
#
# class APIKeyAuthentication(BaseAuthentication):
#     def authenticate(self, request):
#         api_key = request.headers.get('X-API-KEY')
#         if not api_key:
#             return None      # → let JWTAuthentication run next
#
#         try:
#             sub = Subscription.objects.get(api_key=api_key, is_active=True)
#             sub.increment_usage()
#         except Subscription.DoesNotExist:
#             raise AuthenticationFailed('Invalid or inactive API key')
#         except Exception as e:
#             raise AuthenticationFailed(str(e))
#
#         # Attach both subscription & user for views
#         request.subscription = sub
#         request.user         = sub.user
#         return (sub.user, None)
#

# subscriptions/authentication.py

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from subscriptions.models import Subscription

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('x-api-key')

        if not api_key:
            raise AuthenticationFailed('API key missing')

        try:
            subscription = Subscription.objects.get(api_key=api_key)
        except Subscription.DoesNotExist:
            raise AuthenticationFailed('Invalid API key')

        request.subscription = subscription
        return (None, None)

