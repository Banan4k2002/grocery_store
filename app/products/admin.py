from django.contrib import admin

from products.models import Category, Product, Subcategory


class BaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    pass


@admin.register(Subcategory)
class SubcategoryAdmin(BaseAdmin):
    list_filter = ('category',)


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    list_display = ('title', 'slug', 'price')
    list_filter = ('subcategory', 'subcategory__category')
