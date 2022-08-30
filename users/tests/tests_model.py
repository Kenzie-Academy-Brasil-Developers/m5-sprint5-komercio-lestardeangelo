from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractUser
from django.test import TestCase
from users.models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.email = "user_test@mail.com"
        cls.password = "1234"
        cls.first_name = "user"
        cls.last_name = "test"
        cls.is_seller = True

        cls.user_obj: User = User.objects.create_user(
            email=cls.email,
            password=cls.password,
            first_name=cls.first_name,
            last_name=cls.last_name,
            is_seller=cls.is_seller,
        )

    def test_user_fields(self):
        self.assertIsInstance(self.user_obj.email, str)
        self.assertEqual(self.user_obj.email, self.email)

        self.assertIsInstance(self.user_obj.password, str)
        self.assertTrue(check_password(self.password, self.user_obj.password))

        self.assertIsInstance(self.user_obj.first_name, str)
        self.assertEqual(self.user_obj.first_name, self.first_name.title())

        self.assertIsInstance(self.user_obj.last_name, str)
        self.assertEqual(self.user_obj.last_name, self.last_name.title())

        self.assertIsInstance(self.user_obj.is_seller, bool)
        self.assertEqual(self.user_obj.is_seller, self.is_seller)

        self.assertIsInstance(self.user_obj, AbstractUser)
