from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status

from users.serializers import AccountSerializer
from users.models import Account


class TestAccountRegisterView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.base_url = reverse("account-register")
        cls.login_url = reverse("login")

        cls.account_data_1 = {
            "username": "cloud",
            "password": "1234",
            "first_name": "cloud",
            "last_name": "thorson",
            "is_seller": True
        }

        cls.account_data_2 = {
            "username": "odin",
            "password": "1234",
            "first_name": "odin",
            "last_name": "allfather",
            "is_seller": False
        }

        cls.account_data_3 = {
            "username": "fail",
            "senha": "1234",
            "name": "odin",
            "last_name": "allfather",
            "is_seller": True
        }

        cls.account_data_4 = {
            "username": "fail",
            "senha": "1234",
            "name": "odin",
            "last_name": "allfather",
            "is_seller": False
        }

        cls.expected_return_fields =(
            "id",
            "username",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
            "is_superuser"
        )

    
    def test_can_register_seller_account(self):
        print("Test create account with user type seller")

        response = self.client.post(self.base_url,self.account_data_1)

        response_return_fields = tuple(response.data.keys())

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['is_seller'], True)
        self.assertTupleEqual(response_return_fields, self.expected_return_fields)
    

    def test_can_register_non_seller_account(self):
        print("Test create account with user non seller typer")

        response = self.client.post(self.base_url, self.account_data_2)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['is_seller'], False)


    def test_fail_to_register_account_with_wrong_keys(self):
        print("Test should not create account with wrong keys, seller")

        response_seller = self.client.post(self.base_url, self.account_data_3)

        serializer_seller = AccountSerializer(data=self.account_data_3)

        serializer_seller.is_valid()

        self.assertEqual(response_seller.status_code, 400)

        self.assertEqual(response_seller.data, serializer_seller.errors)
    

    def test_fail_to_register_account_with_wrong_keys_non_seller(self):
        print("Test should not create account with wrong keys, non seller")

        response_non_seller = self.client.post(self.base_url, self.account_data_4)

        serializer_non_seller = AccountSerializer(data=self.account_data_4)

        serializer_non_seller.is_valid()

        self.assertEqual(response_non_seller.status_code, 400)

        self.assertEqual(response_non_seller.data, serializer_non_seller.errors)


    def test_login_returns_token_seller(self):
        print("Test token return from login, seller")

        Account.objects.create_user(**self.account_data_1)

        response = self.client.post(self.login_url, self.account_data_1)

        self.assertEqual(200, response.status_code)
        self.assertIn("token", response.data)

    
    def test_login_returns_token_non_seller(self):
        print("Test token return from login, non seller")

        Account.objects.create_user(**self.account_data_2)

        response = self.client.post(self.login_url, self.account_data_2)

        self.assertEqual(200, response.status_code)
        self.assertIn("token", response.data)
    

    def test_anyone_can_list_accounts(self):
        print("Test anyone can list accounts")
        self.client.post(self.base_url,self.account_data_1)
        self.client.post(self.base_url,self.account_data_2)

        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        

class TestAccountUpdateView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.account_data_1 = {
            "username": "cloud",
            "password": "1234",
            "first_name": "cloud",
            "last_name": "thorson",
            "is_seller": True
        }

        cls.account_data_2 = {
            "username": "odin",
            "password": "1234",
            "first_name": "odin",
            "last_name": "allfather",
            "is_seller": False
        }

        cls.admin_account_data = {
            "username": "thor",
            "password": "1234",
            "first_name": "thor",
            "last_name": "odinson",
            "is_seller": False
        }

        account_owner = Account.objects.create_user(**cls.account_data_1)
        account_regular = Account.objects.create_user(**cls.account_data_2)
        admin_account = Account.objects.create_superuser(**cls.admin_account_data)

        cls.account_owner_token = Token.objects.create(user=account_owner)
        cls.account_regular_token = Token.objects.create(user=account_regular)
        cls.admin_token = Token.objects.create(user=admin_account)

        cls.update_url = reverse("account-update", kwargs={"pk": account_owner.id})
        cls.manager_url = reverse("account-manager", kwargs={"pk": account_owner.id})

        cls.data_to_update = {
            "first_name": "first updated",
            "last_name": "last updated"
        }

        cls.data_to_deactivate = {
            "is_active": False
        }

    def test_account_owner_can_edit_profile(self):
        print("Test account owner can edit profile")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.account_owner_token.key)
        response = self.client.patch(self.update_url, self.data_to_update)
        
        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(self.data_to_update["first_name"], response.data["first_name"])
        self.assertEqual(self.data_to_update["last_name"], response.data["last_name"])


    def test_profile_can_not_be_edit_by_non_account_owner(self):
        print("Test user can not edit profile of another account")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.account_regular_token.key)
        response = self.client.patch(self.update_url, self.data_to_update)

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)


    def test_admin_can_deactivate_account(self):
        print("Test admin can deactivate account")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)
        response = self.client.patch(self.manager_url, self.data_to_deactivate)

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(response.data["is_active"], self.data_to_deactivate["is_active"])

 
    def test_admin_can_activate_account(self):
        print("Test admin can activate account")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)
        self.client.patch(self.manager_url, self.data_to_deactivate)

        response = self.client.patch(self.manager_url, {"is_active": True})

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(response.data["is_active"], True)


    def test_non_admin_can_not_deactivate_account(self):
        print("Test non admin can not deactivate account")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.account_regular_token.key)
        response = self.client.patch(self.manager_url, self.data_to_deactivate)
        
        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)


    def test_non_admin_can_not_activate_account(self):
        print("Test non admin can not activate account")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)
        self.client.patch(self.manager_url, self.data_to_deactivate)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.account_regular_token.key)
        response = self.client.patch(self.manager_url, {"is_active": True})

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)