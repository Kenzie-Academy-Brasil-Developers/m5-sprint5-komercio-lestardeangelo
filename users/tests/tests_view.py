from faker import Faker
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from users.models import User


class UserViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        fake = Faker()

        cls.url = "/api/accounts/"
        cls.user_data_seller = {
            "email": "seller_test@mail.com",
            "password": "1234",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "is_seller": True,
        }
        cls.user_data_not_seller = {
            "email": "not_seller_test@mail.com",
            "password": "1234",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "is_seller": False,
        }

    def test_create_user_seller(self) -> None:

        response = self.client.post(self.url, self.user_data_seller, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertNotIn("password", response.json())
        self.assertEqual(response.json()["is_seller"], True)

    def test_create_user_not_seller(self) -> None:

        response = self.client.post(self.url, self.user_data_not_seller, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertNotIn("password", response.json())
        self.assertEqual(response.json()["is_seller"], False)

    def test_create_user_fails_with_invalid_data(self):

        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["email"], ["This field is required."])
        self.assertEqual(response.json()["password"], ["This field is required."])
        self.assertEqual(response.json()["first_name"], ["This field is required."])
        self.assertEqual(response.json()["last_name"], ["This field is required."])
        self.assertEqual(response.json()["is_seller"], ["This field is required."])

        self.assertIn("password", response.json())

    def test_create_user_fails_with_invalid_data_type(self):

        invalid_data_type = {
            "email": "test",
            "password": True,
            "first_name": 1234,
            "last_name": 1234,
            "is_seller": "test",
        }

        response = self.client.post(self.url, invalid_data_type, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["email"], ["Enter a valid email address."])
        self.assertEqual(response.json()["is_seller"], ["Must be a valid boolean."])

    def test_list_users(self) -> None:

        user_seller = User.objects.create(**self.user_data_seller)
        user_not_seller = User.objects.create(**self.user_data_not_seller)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)


class LoginViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        fake = Faker()
        cls.url = "/api/login/"

        cls.user_seller_data = {
            "email": "seller_test@mail.com",
            "password": "1234",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "is_seller": True,
        }

        cls.user_not_seller_data = {
            "email": "not_seller_test@mail.com",
            "password": "1234",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "is_seller": False,
        }

        cls.valid_seller_data_login = {
            "email": "seller_test@mail.com",
            "password": "1234",
        }

        cls.valid_not_seller_data_login = {
            "email": "not_seller_test@mail.com",
            "password": "1234",
        }

        cls.invalid_user_data_login = {
            "email": "invalid_seller_test@mail.com",
            "password": "12344654657",
        }

    def setUp(self) -> None:
        User.objects.create_user(**self.user_seller_data)
        User.objects.create_user(**self.user_not_seller_data)

    def test_login_seller(self):
        response = self.client.post(
            self.url, self.valid_seller_data_login, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_login_not_seller(self):
        response = self.client.post(
            self.url, self.valid_not_seller_data_login, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_login_fail_invalid_credentials(self):
        response = self.client.post(
            self.url, self.invalid_user_data_login, format="json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(response.json(), {"detail": "Invalid email or password."})

    def test_login_fail_invalid_body(self):
        response = self.client.post(self.url, {"email": "email@mail.com"})

        self.assertEqual(response.status_code, 400)
        self.assertIn("password", response.json())


class UserDetailViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.fake = Faker()
        cls.url_login = "/api/login/"
        cls.url_create = "/api/accounts/"
        cls.user_data = {
            "email": "seller_test@mail.com",
            "password": "1234",
            "first_name": cls.fake.first_name(),
            "last_name": cls.fake.last_name(),
            "is_seller": True,
        }

        cls.user = User.objects.create_user(**cls.user_data)
        cls.token = Token.objects.create(user=cls.user)

        cls.other_user_data = {
            "email": "other_test@mail.com",
            "password": "1234",
            "first_name": cls.fake.first_name(),
            "last_name": cls.fake.last_name(),
            "is_seller": False,
        }

        cls.other_user = User.objects.create_user(**cls.other_user_data)
        cls.other_token = Token.objects.create(user=cls.other_user)

    def test_update_account_by_owner(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        user_data_update = {
            "email": "test_seller@mail.com",
            "password": "4321",
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
        }

        response = self.client.patch(
            path=f"{self.url_create}{self.user.id}/",
            data=user_data_update,
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["first_name"], user_data_update["first_name"])
        self.assertEqual(response.json()["last_name"], user_data_update["last_name"])
        self.assertEqual(response.json()["email"], user_data_update["email"])

    def test_fails_update_account_by_not_owner(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.other_token.key)

        user_data_update = {
            "email": "test_seller@mail.com",
            "password": "4321",
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
        }

        response = self.client.patch(
            path=f"{self.url_create}{self.user.id}/",
            data=user_data_update,
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You do not have permission to perform this action."},
        )

    def test_fails_update_account_with_out_token(self):

        user_data_update = {
            "email": "test_seller@mail.com",
            "password": "4321",
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
        }

        response = self.client.patch(
            path=f"{self.url_create}{self.user.id}/",
            data=user_data_update,
            format="json",
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(), {"detail": "Authentication credentials were not provided."}
        )

    def test_fails_update_account_with_an_invalid_token(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.other_token.key[:-1])

        user_data_update = {
            "email": "test_seller@mail.com",
            "password": "4321",
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
        }

        response = self.client.patch(
            path=f"{self.url_create}{self.user.id}/",
            data=user_data_update,
            format="json",
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Invalid token."})


class UserAdminManageAccountViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.fake = Faker()

        cls.account_data_activate = {"is_active": True}

        cls.account_data_deactivate = {"is_active": False}

        cls.admin_data = {
            "email": "admin_test@mail.com",
            "password": "1234",
            "first_name": cls.fake.first_name(),
            "last_name": cls.fake.last_name(),
        }

        cls.admin = User.objects.create_superuser(**cls.admin_data)
        cls.admin_token = Token.objects.create(user=cls.admin)

        cls.not_admin_data = {
            "email": "not_admin_test@mail.com",
            "password": "1234",
            "first_name": cls.fake.first_name(),
            "last_name": cls.fake.last_name(),
            "is_seller": False,
        }

        cls.not_admin = User.objects.create_user(**cls.not_admin_data)
        cls.not_admin_token = Token.objects.create(user=cls.not_admin)

        cls.url = f"/api/accounts/{cls.not_admin.id}/management/"

    def test_fails_deactivate_account_with_a_not_admin_token(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.not_admin_token.key)

        response = self.client.patch(
            path=self.url,
            data=self.account_data_deactivate,
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You do not have permission to perform this action."},
        )

    def test_fails_activate_account_with_a_not_admin_token(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.not_admin_token.key)

        response = self.client.patch(
            path=self.url,
            data=self.account_data_activate,
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You do not have permission to perform this action."},
        )

    def test_deactivate_account_with_a_admin_token(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.patch(
            path=self.url,
            data=self.account_data_deactivate,
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], str(self.not_admin.id))
        self.assertEqual(response.json()["email"], self.not_admin.email)
        self.assertNotEqual(response.json()["is_active"], self.not_admin.is_active)
        self.assertEqual(response.json()["is_active"], self.account_data_deactivate['is_active'])

    def test_activate_account_with_a_admin_token(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.patch(
            path=self.url,
            data=self.account_data_activate,
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], str(self.not_admin.id))
        self.assertEqual(response.json()["email"], self.not_admin.email)
        self.assertEqual(response.json()["is_active"], self.not_admin.is_active)
        self.assertNotEqual(response.json()["is_active"], self.account_data_deactivate['is_active'])


