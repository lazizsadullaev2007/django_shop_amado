from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(verbose_name='Category name', max_length=155, unique=True)

    def __str__(self):
        return self.name

class Brands(models.Model):
    name = models.CharField(verbose_name='Brand name', max_length=155, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    def make_preview_path(self, filename):
        return f'products/preview/{filename}'

    class ProductOptionChoices(models.TextChoices):
        NEW = ('new', 'new')
        POPULAR = ('popular', 'popular')

        __empty__ = ''

    name = models.CharField(max_length=155, verbose_name='Название продукта')
    price = models.IntegerField(verbose_name='Price of product')
    description = models.TextField(verbose_name='Description of product')
    quantity = models.IntegerField(verbose_name='Quantity of product', default='10')
    preview = models.ImageField(verbose_name='Preview of product', upload_to=make_preview_path)
    condition = models.CharField(verbose_name='Condition of product', choices=ProductOptionChoices.choices,
                                 max_length=10, blank=True)
    slug = models.SlugField(default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category of product', related_name='products')
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE, verbose_name='Brand of product', related_name='products')

    def __str__(self):
        return self.name

    def get_preview(self):
        if self.preview:
            return self.preview.url

    def add_to_cart(self):
        return reverse('cart:to_cart', kwargs={'product_id': self.pk, 'action': 'add'})


class ProductImage(models.Model):
    def make_preview_path(self, filename):
        return f'products/images/{filename}'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(verbose_name='Image', upload_to=make_preview_path)



