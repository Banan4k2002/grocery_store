from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import ValidationError

from products.models import Category, Product
from shopping_cart.models import ShoppingCart


class CategorySerializer(serializers.ModelSerializer):
    parent_category = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('title', 'slug', 'image', 'parent_category')

    def get_parent_category(self, obj):
        if isinstance(obj, Category):
            return None
        return obj.category.title


class ProductSerializer(serializers.ModelSerializer):
    subcategory = serializers.StringRelatedField()
    category = serializers.CharField(source='subcategory.category')
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'title',
            'slug',
            'category',
            'subcategory',
            'price',
            'images',
        )

    def get_images(self, obj):
        request = self.context['request']
        images = (
            request.build_absolute_uri(obj.image_small.url),
            request.build_absolute_uri(obj.image_medium.url),
            request.build_absolute_uri(obj.image_large.url),
        )
        return images


class ShoppingCartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ('product', 'quantity')

    def create(self, validated_data):
        product = get_object_or_404(
            Product, pk=self.context['view'].kwargs.get('pk')
        )
        user = self.context['request'].user
        validated_data['product'] = product
        validated_data['user'] = user
        return ShoppingCart.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance

    def validate(self, data):
        request = self.context['request']
        product = get_object_or_404(
            Product, pk=self.context['view'].kwargs.get('pk')
        )
        user = request.user
        data['product'] = product
        data['user'] = user
        if (
            request.method == 'POST'
            and ShoppingCart.objects.filter(
                product=data['product'],
                user=data['user'],
            ).exists()
        ):
            raise ValidationError({'errors': 'Продукт уже добавлен в корзину'})
        return data


class ShoppingCartListSerializer(serializers.Serializer):
    products = ShoppingCartSerializer(many=True)
    total_quantity = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
