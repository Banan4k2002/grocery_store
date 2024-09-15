from rest_framework import serializers

from products.models import Category, Product


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
