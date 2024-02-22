from users.models import CustomUser
from shop import settings

from store.models import Product
from .models import Order, OrderProduct


class CartForAuthenticatedUser:
    def __init__(self, request, product_id=None, action=None):
        self.user = request.user

        if product_id and action:
            self.add_or_delete(product_id, action)

    def get_cart_info(self):
        user, created = CustomUser.objects.get_or_create(
            username=self.user.username,
            email=self.user.email
        )

        order, created = Order.objects.get_or_create(
            user=user
        )

        order_products = order.orderproduct_set.all()
        return {
            'cart_total_quantity': order.get_cart_total_quantity,
            'cart_total_price': order.get_cart_total_price,
            'products': order_products,
            'order': order
        }

    def add_or_delete(self, product_id, action):
        order = self.get_cart_info()['order']
        product = Product.objects.get(pk=product_id)
        order_product, created = OrderProduct.objects.get_or_create(
            order=order,
            product=product
        )
        if action == 'add' and product.quantity > 0:
            order_product.quantity += 1
            product.quantity -= 1
        else:
            order_product.quantity -= 1
            product.quantity += 1

        order_product.save()
        product.save()
        if order_product.quantity <= 0:
            order_product.delete()

    def clear(self):
        products = self.get_cart_info()['products']
        order = self.get_cart_info()['order']
        for product in products:
            product.delete()
        order.save()


class CartForAnonymousUser:
    def __init__(self, request, product_id=None, action=None):
        self.session = request.session
        self.cart = self.get_cart()

        if product_id and action:
            self.key = str(product_id)
            self.product = Product.objects.get(pk=product_id)
            self.cart_product = self.cart.get(self.key)

            if action == 'add' and self.product.quantity > 0:
                self.add()
            else:
                self.delete()

            self.product.save()
            self.save()

    def get_cart(self):
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session['cart'] = {}
        return cart

    def save(self):
        self.session.modified = True

    def get_cart_info(self):
        products = []
        order = {
            'get_cart_total_quantity': 0,
            'get_cart_total_price': 0
        }
        cart_total_quantity = order['get_cart_total_quantity']
        cart_total_price = order['get_cart_total_price']

        for key in self.cart:
            if self.cart[key]['quantity'] > 0:
                product_qty = self.cart[key]['quantity']
                cart_total_quantity += product_qty
                product = Product.objects.get(pk=key)
                get_total_price = product.price * product_qty

                cart_product = {
                    'pk': product.pk,
                    'product': {
                        'pk': product.pk,
                        'name': product.name,
                        'price': product.price,
                        'slug': product.slug,
                        'get_preview': product.get_preview(),
                        'quantity': product.quantity
                    },
                    'quantity': product_qty,
                    'get_total_price': get_total_price
                }
                products.append(cart_product)
                order['get_cart_total_price'] += cart_product['get_total_price']
                order['get_cart_total_quantity'] += cart_product['quantity']
                cart_total_price = order['get_cart_total_price']
        self.save()
        return {
            'cart_total_quantity': cart_total_quantity,
            'cart_total_price': cart_total_price,
            'products': products,
            'order': order
        }


    def add(self):
        if self.cart_product:
            self.cart_product['quantity'] += 1
        else:
            self.cart[self.key] = {
                'quantity': 1
            }
        self.product.quantity -= 1

    def delete(self):
        self.cart_product['quantity'] -= 1
        self.product.quantity += 1

        if self.cart_product['quantity'] <= 0:
            del self.cart[self.key]

    def clear(self):
        self.cart.clear()


def get_cart_data(request):
    if request.user.is_authenticated:
        user_cart = CartForAuthenticatedUser(request)
        cart_info = user_cart.get_cart_info()
    else:
        session_cart = CartForAnonymousUser(request)
        cart_info = session_cart.get_cart_info()

    return {
        'cart_total_quantity': cart_info['cart_total_quantity'],
        'cart_total_price': cart_info['cart_total_price'],
        'products': cart_info['products'],
        'order': cart_info['order']
    }

