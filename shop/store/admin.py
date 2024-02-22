from django.contrib import admin

from .models import Brands, Category,Product, ProductImage

# Register your models here.

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ]
    prepopulated_fields = {'slug': ('name', )}



admin.site.register(Category)
admin.site.register(Brands)
admin.site.register(Product, ProductAdmin)
