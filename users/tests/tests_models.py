from django.db.utils import IntegrityError
from django.test import TestCase
from products.models import Product
from users.models import Account


class AccountModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.account_data = {
            "username": "odin",
            "first_name": "odin",
            "last_name": "allfather",
            "is_seller": True
        }

        cls.product_data = {
            "description": "generic product",
            "price": 100.00,
            "quantity": 2,
            "is_active": True
        }

        cls.account = Account.objects.create(**cls.account_data)
        cls.products = [Product.objects.create(**cls.product_data, seller=cls.account) for _ in range(10)]


    def test_account_fields(self):
        print("Test for account fields")    

        self.assertEqual(self.account_data["username"], self.account.username)
        self.assertEqual(self.account_data["first_name"], self.account.first_name)
        self.assertEqual(self.account_data["last_name"], self.account.last_name)
        self.assertEqual(self.account_data["is_seller"], self.account.is_seller)
    
    
    def test_account_fields_parameters(self):
        print("Test for account fields parameters")

        account_test = Account.objects.get(username="odin")

        username_max_length = account_test._meta.get_field("username").max_length
        first_name_max_length = account_test._meta.get_field("first_name").max_length
        last_name_max_length = account_test._meta.get_field("last_name").max_length

        self.assertEqual(username_max_length, 50)
        self.assertEqual(first_name_max_length, 50)
        self.assertEqual(last_name_max_length, 50)
    

    def test_account_can_have_multiple_products(self):
        print("Test if account can contain multiple products")

        self.assertEqual(len(self.products), self.account.products.count())

        for product in self.products:
            self.assertEqual(self.account, product.seller)

    
    def test_account_should_have_unique_username(self):
        print("Test fail to create account with the same username")
        with self.assertRaises(IntegrityError):
            Account.objects.create(**self.account_data)
