from uuid import UUID

from accounts.models import Account
from django.test import TestCase
from faker import Faker
from products.models import Product


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        fake = Faker()

        cls.description = fake.paragraph(nb_sentences=2)
        cls.price = fake.pyfloat(
            right_digits=2,
            positive=True,
            min_value=0.01,
            max_value=100,
        )
        cls.quantity = fake.pyint(
            min_value=1,
            max_value=100,
        )
        cls.seller: Account = Account.objects.create_user(
            email=fake.ascii_company_email(),
            password=fake.password(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            is_seller=True,
        )
        cls.product_obj: Product = Product.objects.create(
            description=cls.description,
            price=cls.price,
            quantity=cls.quantity,
            seller=cls.seller,
        )

    def test_product_fields(self):
        self.assertIsInstance(self.product_obj.id, UUID)

        self.assertIsInstance(self.product_obj.description, str)
        self.assertEqual(self.product_obj.description, self.description)

        self.assertIsInstance(self.product_obj.price, float)
        self.assertEqual(self.product_obj.price, self.price)

        self.assertIsInstance(self.product_obj.quantity, int)
        self.assertEqual(self.product_obj.quantity, self.quantity)

        self.assertIsInstance(self.product_obj.is_active, bool)
        self.assertTrue(self.product_obj.is_active)

        self.assertIsInstance(self.product_obj.seller, Account)
        self.assertTrue(self.product_obj.seller.is_seller)
