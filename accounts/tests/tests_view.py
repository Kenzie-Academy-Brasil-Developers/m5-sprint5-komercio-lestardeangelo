from accounts.models import Account
from faker import Faker
from rest_framework.test import APITestCase


class AccountViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        faker = Faker()
        cls.url = "/api/accounts/"
        cls.account_data_seller = {
            "email": faker.ascii_company_email(),
            "password": faker.password(length=12),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "is_seller": True,
        }
        cls.account_data_not_seller = {
            "email": faker.ascii_company_email(),
            "password": faker.password(length=12),
            "first_name": faker.first_name(),
            "password": "123456789",
            "last_name": faker.last_name(),
        }
        cls.invalid_account_data_seller = {
            "email": faker.ascii_company_email(),
            "password": faker.password(length=12),
            "last_name": faker.last_name(),
            "is_seller": True,
        }
        cls.invalid_account_data_not_seller = {
            "email": faker.ascii_company_email(),
            "password": faker.password(length=12),
            "last_name": faker.last_name(),
        }

    def test_create_account_seller(self) -> None:
        response = self.client.post(self.url, self.account_data_seller)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("is_seller"), True)
        self.assertNotIn("password", response.json())
        self.assertIn("date_joined", response.json())

    def test_create_account_not_seller(self) -> None:
        response = self.client.post(self.url, self.account_data_not_seller)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("is_seller"), False)
        self.assertNotIn("password", response.json())
        self.assertIn("date_joined", response.json())

    def test_create_account_invalid_data_seller_fails(self) -> None:
        response = self.client.post(self.url, self.invalid_account_data_seller)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get("first_name"), ["This field is required."])

    def test_create_account_invalid_data_not_seller_fails(self) -> None:
        response = self.client.post(self.url, self.invalid_account_data_not_seller)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get("first_name"), ["This field is required."])

    def test_create_account_email_already_existis_fails(self) -> None:
        self.client.post(self.url, self.account_data_not_seller)
        response = self.client.post(self.url, self.account_data_not_seller)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data.get("email"), ["user with this email already exists."]
        )


class LoginViewNotSellerTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        faker = Faker()
        cls.url = "/api/login/"
        cls.account_data = {
            "email": faker.ascii_company_email(),
            "password": faker.password(length=12),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
        }
        cls.invalid_user_data = {
            "email": cls.account_data.get("email"),
            "password": "123456789",
        }

    def setUp(self) -> None:
        Account.objects.create_user(**self.account_data)

    def test_not_seller_login_successful(self):
        response = self.client.post(self.url, self.account_data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_login_not_seller_fail_invalid_credentials(self):
        response = self.client.post(self.url, self.invalid_user_data)

        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(
            response.json(),
            {"detail": "Invalid email or password."},
        )

    def test_login_not_seller_fail_invalid_body(self):
        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(
            response.json(),
            {
                "email": ["This field is required."],
                "password": ["This field is required."],
            },
        )


class LoginViewSellerTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        faker = Faker()
        cls.url = "/api/login/"
        cls.account_data = {
            "email": faker.ascii_company_email(),
            "password": faker.password(length=12),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "is_seller": True,
        }
        cls.invalid_user_data = {
            "email": cls.account_data.get("email"),
            "password": "123456789",
        }

    def setUp(self) -> None:
        Account.objects.create_user(**self.account_data)

    def test_seller_login_successful(self):
        response = self.client.post(self.url, self.account_data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_login_seller_fail_invalid_credentials(self):
        response = self.client.post(self.url, self.invalid_user_data)

        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(
            response.json(),
            {"detail": "Invalid email or password."},
        )

    def test_login_seller_fail_invalid_body(self):
        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(
            response.json(),
            {
                "email": ["This field is required."],
                "password": ["This field is required."],
            },
        )


class ListAccountsTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.url = "/api/accounts/"

    def test_anyone_can_list_all_accoutns(self) -> None:
        response = self.client.get(self.url)

        self.assertIsInstance(response.json(), list)


# class UpdateAccountViewTest(APITestCase):
#     @classmethod
#     def setUpTestData(cls) -> None:
#         faker = Faker()
#         cls.url_login = "/api/login/"
#         cls.url = "/api/accounts/<pk>/management/"
#         cls.account_data_admin = {
#             "email": faker.ascii_company_email(),
#             "password": faker.password(length=12),
#             "first_name": faker.first_name(),
#             "last_name": faker.last_name(),
#         }
#         cls.account_data = {
#             "email": faker.ascii_company_email(),
#             "password": faker.password(length=12),
#             "first_name": faker.first_name(),
#             "last_name": faker.last_name(),
#         }

#     def setUp(self) -> None:
#         self.normal_account: Account = Account.objects.create_user(**self.account_data)
#         self.admin_account: Account = Account.objects.create_user(
#             **self.account_data_admin
#         )
#         self.admin_account.is_staff = True
#         self.admin_account.is_superuser = True
#         self.admin_account.save()

#     def test_admin_can_deactivate_account(self) -> None:
#         login_response = self.client.post(self.url_login, self.account_data_admin)

#         self.url = f"/api/accounts/{self.normal_account.id}/management/"

#         response = self.client.patch(
#             path=self.url,
#             data={"is_active": True},
#         )
