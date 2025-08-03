from django.contrib import admin
from .models import Plan, Subscription

admin.site.register(Plan)    

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'plan', 'api_key', 'is_active',
        'usage_count', 'reset_at', 'created_at', 'updated_at'
    ]
    readonly_fields = ['created_at', 'updated_at', 'api_key']  
    search_fields = ['user__username', 'api_key']  
    list_filter = ['is_active', 'plan']  
