from uuid import UUID
from faker import Faker

from accounts.models import Account
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractUser
from django.test import TestCase


class AccountModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        fake = Faker()
        cls.email = fake.ascii_company_email()
        cls.password = fake.password()
        cls.first_name = fake.first_name()
        cls.last_name = fake.last_name()
        cls.account_obj: Account = Account.objects.create_user(
            email=cls.email,
            password=cls.password,
            first_name=cls.first_name,
            last_name=cls.last_name,
        )

    def test_account_fields(self):
        self.assertIsInstance(self.account_obj.id, UUID)

        self.assertIsInstance(self.account_obj.email, str)
        self.assertEqual(self.account_obj.email, self.email)

        self.assertIsInstance(self.account_obj.first_name, str)
        self.assertEqual(self.account_obj.first_name, self.first_name.title())

        self.assertIsInstance(self.account_obj.last_name, str)
        self.assertEqual(self.account_obj.last_name, self.last_name.title())

        self.assertIsInstance(self.account_obj.password, str)
        self.assertTrue(check_password(self.password, self.account_obj.password))

        self.assertIsInstance(self.account_obj.is_seller, bool)
        self.assertFalse(self.account_obj.is_seller)

        self.assertIsInstance(self.account_obj, AbstractUser)
