from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
import secrets
import uuid 

User = get_user_model()

class Plan(models.Model):
    """
    Represents a subscription tier (e.g., Free, Pro, Enterprise).
    Use 'slug' to map internally or to external services like Stripe.
    """
    slug = models.SlugField(
        unique=True,
        help_text="Unique identifier for this plan (e.g., 'free', 'pro', 'enterprise')"
    )
    name = models.CharField(
        max_length=50,
        help_text="Display name for the plan (e.g., 'Pro Plan')"
    )
    description = models.TextField(
        blank=True,
        help_text="Optional description of the plan and its features."
    )
    api_quota = models.PositiveIntegerField(
        help_text="Maximum number of API calls allowed per period."
    )
    period_days = models.PositiveIntegerField(
        default=30,
        help_text="Number of days after which quota resets (default: 30 days)."
    )

    class Meta:
        verbose_name = "Subscription Plan"
        verbose_name_plural = "Subscription Plans"
        ordering = ["api_quota"]

    def __str__(self):
        return f"{self.name} ({self.slug})"

class Subscription(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='subscription'
    )
    plan = models.ForeignKey(
        'Plan',  # Use string reference to avoid import issues
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    api_key = models.CharField(
        max_length=64,
        unique=True,
        editable=False,
        blank=True  # Allow blank during creation
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the subscription is active or not."
    )
    usage_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of API calls used in the current period."
    )
    reset_at = models.DateTimeField(
        null=True,  # Allow null during creation
        blank=True,
        help_text="Date and time when the current period will reset."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Subscription Profile"
        verbose_name_plural = "Subscription Profiles"

    def save(self, *args, **kwargs):
        
        # Ensure the subscription has a valid plan
        if not self.plan:
            try:
                self.plan = Plan.objects.get(slug='free')
            except Plan.DoesNotExist:
                raise ValidationError("Default 'free' plan does not exist.")
            
        # Generate the API key if not already set
        if not self.api_key:
            self.api_key = self._generate_unique_api_key()

        # Calculate the reset_at date based on the plan's period_days
        if self.plan and hasattr(self.plan, 'period_days') and self.plan.period_days:
            self.reset_at = timezone.now() + timezone.timedelta(days=self.plan.period_days)
        else:
            raise ValidationError("The plan's period_days is invalid or missing.")
        
        super().save(*args, **kwargs)

    def _generate_unique_api_key(self):
        """Generate a unique API key."""
        max_attempts = 10
        for _ in range(max_attempts):
            api_key = secrets.token_urlsafe(48)  # 48 chars to ensure it fits in 64 char field
            if not Subscription.objects.filter(api_key=api_key).exists():
                return api_key
        raise ValidationError("Failed to generate unique API key after multiple attempts.")

    def rotate_key(self):
        """Rotate the API key for this subscription."""
        self.api_key = self._generate_unique_api_key()
        self.save(update_fields=['api_key', 'updated_at'])

    def increment_usage(self):
        """Increment usage count and handle quota limits."""
        now = timezone.now()
        
        # Check if we need to reset the usage period
        if self.reset_at and now > self.reset_at:
            self.usage_count = 0
            # Fixed the typo: was "now = timezone.timedelta", should be "now + timezone.timedelta"
            self.reset_at = now + timezone.timedelta(days=self.plan.period_days)
        
        # Increment usage
        self.usage_count += 1
        
        # Check quota limit
        if hasattr(self.plan, 'api_quota') and self.usage_count > self.plan.api_quota:
            self.is_active = False
            self.save(update_fields=['usage_count', 'is_active', 'reset_at', 'updated_at'])
            raise ValidationError('Subscription has reached its quota limit.')
        
        self.save(update_fields=['usage_count', 'reset_at', 'updated_at'])

    def is_quota_exceeded(self):
        """Check if the subscription has exceeded its quota."""
        if not hasattr(self.plan, 'api_quota'):
            return False
        return self.usage_count >= self.plan.api_quota

    def days_until_reset(self):
        """Calculate days until the next reset."""
        if not self.reset_at:
            return None
        now = timezone.now()
        if now > self.reset_at:
            return 0
        return (self.reset_at - now).days

    def __str__(self):
        return f"{self.user.full_name}'s subscription profile ({self.plan.name if hasattr(self.plan, 'name') else 'Unknown Plan'})"

