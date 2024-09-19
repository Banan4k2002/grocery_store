from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from products.consts import (
    LARGE_IMAGE_HEIGHT,
    LARGE_IMAGE_WIDTH,
    MEDIUM_IMAGE_HEIGHT,
    MEDIUM_IMAGE_WIDTH,
    SLUG_MAX_LENGTH,
    SMALL_IMAGE_HEIGHT,
    SMALL_IMAGE_WIDTH,
    TITLE_MAX_LENGTH,
)


def get_upload_to(instance, filename):
    return f'{instance.__class__.__name__.lower()}s/{filename}'


class BaseModel(models.Model):
    title = models.CharField('Наименование', max_length=TITLE_MAX_LENGTH)
    slug = models.SlugField(
        'slug-имя', max_length=SLUG_MAX_LENGTH, unique=True
    )
    image = models.ImageField('Изображение', upload_to=get_upload_to)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Category(BaseModel):

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'Категории'


class Subcategory(BaseModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='subcategories',
    )

    class Meta:
        verbose_name = 'подкатегорию'
        verbose_name_plural = 'Подкатегории'


class Product(BaseModel):
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        verbose_name='Подкатегория',
        related_name='products',
    )
    price = models.DecimalField(
        'Цена',
        max_digits=10,
        decimal_places=2,
        validators=(MinValueValidator(Decimal(0.00)),),
    )
    image_small = ImageSpecField(
        source='image',
        processors=[ResizeToFill(SMALL_IMAGE_WIDTH, SMALL_IMAGE_HEIGHT)],
    )
    image_medium = ImageSpecField(
        source='image',
        processors=[ResizeToFill(MEDIUM_IMAGE_WIDTH, MEDIUM_IMAGE_HEIGHT)],
    )
    image_large = ImageSpecField(
        source='image',
        processors=[ResizeToFill(LARGE_IMAGE_WIDTH, LARGE_IMAGE_HEIGHT)],
    )

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('id',)
