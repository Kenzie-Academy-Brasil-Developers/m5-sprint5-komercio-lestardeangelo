from itertools import product
from django.test import TestCase
from users.models import Account
from products.models import Product


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.product_data_1 = {
            "description": "generic product",
            "price": 100.00,
            "quantity": 2,
            "is_active": True
        }

        cls.account_data_1 = {
            "username": "odin",
            "first_name": "odin",
            "last_name": "allfather",
            "is_seller": True
        }

        cls.account_data_2 = {
            "username": "thor",
            "first_name": "thor",
            "last_name": "odinson",
            "is_seller": True
        }

        cls.account_1 = Account.objects.create(**cls.account_data_1)
        cls.account_2 = Account.objects.create(**cls.account_data_2)
        cls.product = Product.objects.create(**cls.product_data_1, seller=cls.account_1)
    

    def test_product_fields(self):
        print("Test for product fields")

        self.assertEqual(self.product_data_1["description"], self.product.description)
        self.assertEqual(self.product_data_1["price"], self.product.price)
        self.assertEqual(self.product_data_1["quantity"], self.product.quantity)
        self.assertEqual(self.product_data_1["is_active"], self.product.is_active)

    
    def test_product_fields_parameters(self):
        print("Test for product fields parameters")

        product_test = Product.objects.get(id = self.product.id)
        product_price_max_digits = product_test._meta.get_field("price").max_digits
        product_price_decimal_places = product_test._meta.get_field("price").decimal_places

        self.assertEqual(product_price_max_digits, 10)
        self.assertEqual(product_price_decimal_places, 2)

    def test_product_can_not_have_multiple_sellers(self):
        print("Test if product can not have multiple sellers")
        
        self.assertIn(self.product, self.account_1.products.filter(description="generic product"))
        
        self.account_2.products.add(self.product)
        
        self.assertNotIn(self.product, self.account_1.products.filter(description="generic product"))
        self.assertIn(self.product, self.account_2.products.filter(description="generic product"))


