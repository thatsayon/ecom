from rest_framework import serializers
from mptt.fields import TreeForeignKey
from .models import (
    Category,
    Product,
)


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'children']

    def get_children(self, obj):
        # Get only direct children
        if obj.get_children():
            return CategorySerializer(obj.get_children(), many=True).data
        return []


class ProductSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()
    has_discount = serializers.ReadOnlyField()
    is_in_stock = serializers.SerializerMethodField()

    category = CategorySerializer(read_only=True)
    category_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'category_id',  
            'name',
            'slug',
            'description',
            'price',
            'discount_price',
            'final_price',
            'has_discount',
            'stock',
            'is_in_stock',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'slug',
            'final_price',
            'has_discount',
            'is_in_stock',
            'created_at',
            'updated_at',
            'category'
        ]

    def get_final_price(self, obj):
        return obj.get_final_price()

    def get_is_in_stock(self, obj):
        return obj.is_in_stock()

