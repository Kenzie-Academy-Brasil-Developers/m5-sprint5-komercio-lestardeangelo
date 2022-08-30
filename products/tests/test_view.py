import random
from faker import Faker
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from products.models import Product
from products.serializers import ProductCreateSerializer, ProductListSerializer
from users.models import User


class ProductsViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.fake = Faker()

        cls.url = "/api/products/"

        cls.user_data = {
            "email": "seller_test@mail.com",
            "password": "1234",
            "first_name": cls.fake.first_name(),
            "last_name": cls.fake.last_name(),
            "is_seller": True,
        }

        cls.user = User.objects.create_user(**cls.user_data)
        cls.token = Token.objects.create(user=cls.user)

        cls.user_not_seller_data = {
            "email": "not_seller_test@mail.com",
            "password": "1234",
            "first_name": cls.fake.first_name(),
            "last_name": cls.fake.last_name(),
            "is_seller": False,
        }

        cls.user_not_seller = User.objects.create_user(**cls.user_not_seller_data)
        cls.not_seller_token = Token.objects.create(user=cls.user_not_seller)

        cls.product_data = {
            "description": cls.fake.bothify(text="Product Number: ????-########"),
            "price": round(random.uniform(1.00, 1000.99), 2),
            "quantity": cls.fake.random_int(min=5, max=25),
            "user": cls.user,
        }

        for _ in range(10):
            Product.objects.create(**cls.product_data)

    def test_list_created_products(self):

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 10)

    def test_create_product_with_seller_auth_token(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.post(self.url, self.product_data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["description"], self.product_data["description"]
        )
        self.assertEqual(response.json()["price"], self.product_data["price"])
        self.assertEqual(response.json()["seller"]["id"], str(self.user.id))

    def test_fail_create_product_with_not_seller_auth_token(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.not_seller_token.key)

        response = self.client.post(self.url, self.product_data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You do not have permission to perform this action."},
        )

    def test_fail_create_product_with_out_auth_token(self):

        response = self.client.post(self.url, self.product_data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(), {"detail": "Authentication credentials were not provided."}
        )

    def test_fail_create_product_with_wrong_keys(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(
            response.json(),
            {
                "description": ["This field is required."],
                "price": ["This field is required."],
                "quantity": ["This field is required."],
            },
        )

    def test_fail_create_product_with_negative_quantity_value(self):

        wrong_product_data = {
            "description": self.fake.bothify(text="Product Number: ????-########"),
            "price": round(random.uniform(1.00, 1000.99), 2),
            "quantity": -5,
            "user": self.user,
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.post(self.url, wrong_product_data)

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(
            response.json(),
            {"quantity": ["Ensure this value is greater than or equal to 0."]},
        )

    def test_format_on_create_product(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.post(self.url, self.product_data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(ProductCreateSerializer(data=response.json()))

    def test_format_on_list_products(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        for product in response.json():
            self.assertTrue(ProductListSerializer(data=product))


class ProductIdViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.fake = Faker()

        cls.user_data = {
            "email": "seller_test@mail.com",
            "password": "1234",
            "first_name": cls.fake.first_name(),
            "last_name": cls.fake.last_name(),
            "is_seller": True,
        }

        cls.user = User.objects.create_user(**cls.user_data)
        cls.token = Token.objects.create(user=cls.user)

        cls.user_not_owner_data = {
            "email": "not_owner_test@mail.com",
            "password": "1234",
            "first_name": cls.fake.first_name(),
            "last_name": cls.fake.last_name(),
            "is_seller": True,
        }

        cls.user_not_owner = User.objects.create_user(**cls.user_not_owner_data)
        cls.not_owner_token = Token.objects.create(user=cls.user_not_owner)

        cls.product_data = {
            "description": cls.fake.bothify(text="Product Number: ????-########"),
            "price": round(random.uniform(1.00, 1000.99), 2),
            "quantity": cls.fake.random_int(min=5, max=25),
            "user": cls.user,
        }

        cls.product = Product.objects.create(**cls.product_data)

        cls.url = f"/api/products/{cls.product.product_uuid}/"

    def test_update_product_with_owner_seller_auth_token(self):

        product_update_data = {
            "description": self.fake.bothify(text="Product Number: ????-########"),
            "price": round(random.uniform(1.00, 1000.99), 2),
            "quantity": self.fake.random_int(min=5, max=25),
            "user": self.user,
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.patch(self.url, product_update_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["description"], product_update_data["description"]
        )
        self.assertEqual(response.json()["price"], product_update_data["price"])
        self.assertEqual(response.json()["seller"]["id"], str(self.user.id))

    def test_fail_create_product_with_not_owner_seller_auth_token(self):

        product_update_data = {
            "description": self.fake.bothify(text="Product Number: ????-########"),
            "price": round(random.uniform(1.00, 1000.99), 2),
            "quantity": self.fake.random_int(min=5, max=25),
            "user": self.user,
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.not_owner_token.key)

        response = self.client.patch(self.url, product_update_data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You do not have permission to perform this action."},
        )

    def test_fail_create_product_with_out_auth_token(self):

        product_update_data = {
            "description": self.fake.bothify(text="Product Number: ????-########"),
            "price": round(random.uniform(1.00, 1000.99), 2),
            "quantity": self.fake.random_int(min=5, max=25),
            "user": self.user,
        }

        response = self.client.patch(self.url, product_update_data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(), {"detail": "Authentication credentials were not provided."}
        )

    def test_list_specific_product(self):

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["description"], self.product.description)
