from django.db import models
from users.models import CustomUser
from store.models import Product

# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,
                             null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    @property
    def get_cart_total_price(self):
        products = self.orderproduct_set.all()
        return sum([product.get_total_price for product in products])

    @property
    def get_cart_total_quantity(self):
        products = self.orderproduct_set.all()
        return sum([product.quantity for product in products])


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_price(self):
        return self.product.price * self.quantity

class Customer(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    company_name = models.CharField(max_length=150, verbose_name='Компания')
    email = models.EmailField(max_length=150, verbose_name='Почта')
    state = models.CharField(max_length=100, verbose_name='Штат')
    address = models.CharField(max_length=150, verbose_name='Адрес')
    town = models.CharField(max_length=100, verbose_name='Город')
    zip_code = models.CharField(max_length=100, verbose_name='Зип-код')
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона')
    comment = models.TextField(verbose_name='Комментарий')
