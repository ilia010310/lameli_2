from decimal import Decimal

from django.test import TestCase
from .models import Product, Category

class ProductModelTests(TestCase):
    def setUp(self):
        self.product = Product(
            name='First Product',
            slug='first-product',
            avatar='default.png',
            description='Description of the product',
            status='NO',
            price='2500'
        )

    def test_create_product(self):
        self.assertIsInstance(self.product, Product)

    def test_str_representation(self):
        self.assertEqual(str(self.product), "First Product")

    def test_saving_and_retrieving_product(self):
        first_category = Category(title='Товар', slug='Tovar')
        first_category.save()

        first_product = Product()
        first_product.name = 'First Product'
        first_product.slug = 'first-product'
        first_product.avatar = 'default.png'
        first_product.description = 'Description of the product'
        first_product.status = 'NO'
        first_product.price = '2500'
        first_product.category = first_category
        first_product.save()

        second_product = Product()
        second_product.name = 'Second Product'
        second_product.slug = 'second-product'
        second_product.avatar = 'default.png'
        second_product.description = 'Description of the product2'
        second_product.status = 'YES'
        second_product.price = '3500'
        second_product.category = first_category
        second_product.save()

        saved_products = Product.objects.all()
        self.assertEqual(saved_products.count(), 2)

        first_saved_products = saved_products[0]
        second_saved_products = saved_products[1]
        self.assertEqual(first_saved_products.name, 'First Product')
        self.assertEqual(second_saved_products.price, Decimal('3500'))

