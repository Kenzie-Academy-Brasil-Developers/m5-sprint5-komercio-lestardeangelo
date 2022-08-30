from django.contrib.auth.models import AbstractUser
from django.test import TestCase
from products.models import Product
from users.models import User


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_obj: User = User.objects.create_user(
            email="seller_test@mail.com",
            password="1234",
            first_name="First Seller",
            last_name="None",
            is_seller=True,
        )

        cls.product_data_one = {
            "description": "Iphone 13 Pro Max",
            "price": 13000.99,
            "quantity": 15,
        }

        cls.product_obj_one = Product.objects.create(
            **cls.product_data_one, user=cls.user_obj
        )

        cls.product_data_two = {
            "description": "Apple Dots",
            "price": 1900.99,
            "quantity": 25,
        }

        cls.product_obj_two = Product.objects.create(
            **cls.product_data_two, user=cls.user_obj
        )

    def test_product_fields(self):

        self.assertIsInstance(self.product_obj_one.description, str)
        self.assertEqual(
            self.product_obj_one.description, self.product_data_one["description"]
        )

        self.assertIsInstance(self.product_obj_one.price, float)
        self.assertEqual(self.product_obj_one.price, self.product_data_one["price"])

        self.assertIsInstance(self.product_obj_one.quantity, int)
        self.assertEqual(
            self.product_obj_one.quantity, self.product_data_one["quantity"]
        )

        self.assertIsInstance(self.product_obj_one.is_active, bool)
        self.assertEqual(self.product_obj_one.is_active, True)

        self.assertEqual(self.product_obj_one.user, self.user_obj)
        self.assertIsInstance(self.product_obj_one.user, AbstractUser)

    def test_multiple_products_may_contain_same_user(self):

        self.assertEqual(self.product_obj_one.user, self.user_obj)
        self.assertEqual(self.product_obj_two.user, self.user_obj)
