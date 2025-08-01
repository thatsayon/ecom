from django.urls import path

from .views import (
    SubscriptionCreateView,
    RegenerateAPIKeyView,
)

urlpatterns = [
    path('create/', SubscriptionCreateView.as_view(), name='create'),
    path('regenerate-key/', RegenerateAPIKeyView.as_view(), name='regenerate-key')
]
