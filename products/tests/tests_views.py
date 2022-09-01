from rest_framework.test import APITestCase
from products.models import Product
from users.models import Account
from rest_framework.views import status
from rest_framework.authtoken.models import Token
from django.urls import reverse


class TestProductView(APITestCase):
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
            "username": "krun",
            "password": "1234",
            "first_name": "krun",
            "last_name": "demno",
            "is_seller": False
        }

        cls.account_data_3 = {
            "username": "odin",
            "password": "1234",
            "first_name": "odin",
            "last_name": "allfather",
            "is_seller": True
        }

        cls.product_data = {
            "description": "Smartband XYZ 3.22",
            "price": "100.99",
            "quantity": 15
        }

        cls.product_data_2 = {
            "description": "google home",
            "price": "200.99",
            "quantity": 15
        }

        cls.product_update_data = {
            "description": "updated"
        }

        seller_account = Account.objects.create_user(**cls.account_data_1)
        regular_account = Account.objects.create_user(**cls.account_data_2)
        cls.seller_token = Token.objects.create(user=seller_account)
        cls.regular_token = Token.objects.create(user=regular_account)

        cls.base_url = reverse("product-view")
        cls.detail_url = reverse("product-detail", kwargs={"pk": seller_account.id})

    
    def test_seller_can_create_product(self):
        print("test seller can create a product")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.seller_token.key)
        response = self.client.post(self.base_url, self.product_data)

        expected_status = status.HTTP_201_CREATED
        response_status = response.status_code

        self.assertEqual(expected_status, response_status)
    
    
    def test_create_product_wrong_keys(self):
        print("test create product with wrong keys")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.seller_token.key)
        response = self.client.post(self.base_url, {})

        expected_status = status.HTTP_400_BAD_REQUEST
        response_status = response.status_code

        self.assertEqual(expected_status, response_status)

    
    def test_non_seller_can_not_create_product(self):
        print("test non seller can not create a product")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.regular_token.key)
        response = self.client.post(self.base_url, self.product_data)

        expected_status = status.HTTP_403_FORBIDDEN
        response_status = response.status_code

        self.assertEqual(expected_status, response_status)


    def test_anyone_can_list_product(self):
        print("test anyone can list products")

        response = self.client.get(self.base_url)

        expected_status = status.HTTP_200_OK
        response_status = response.status_code

        self.assertEqual(expected_status, response_status)
        self.assertIn('results', response.data.keys())

    
    def test_create_product_data(self):
        print("test data from create product")
        
        Account.objects.create_user(**self.account_data_3)
        token_response = self.client.post(reverse("login"), self.account_data_3)
        
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_response.data['token'])
        product_response = self.client.post(self.base_url, self.product_data)

        expected_return_fields = (
           "id", 
           "seller",
           "description",
           "price",
           "quantity",
           "is_active"
        )

        account_response = self.client.get(reverse("list-view", kwargs={"num": 1}))
        account_owner = account_response.data['results'][0]

        response_return_fields = tuple(product_response.data.keys())

        self.assertTupleEqual(expected_return_fields, response_return_fields)

        product_response.data.pop("id")
        product_response.data.pop("is_active")

        for key, item in product_response.data.items():
            if key == 'seller':
                for seller_key, seller_item in product_response.data['seller'].items():
                    if seller_key == 'id':
                        continue
                    self.assertEqual(seller_item, account_owner[seller_key])
                continue

            self.assertEqual(item, self.product_data[key])

    
    def test_list_product_data(self):
        print("test data from list products")

        account = Account.objects.create_user(**self.account_data_3)
        token_response = self.client.post(reverse("login"), self.account_data_3)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_response.data['token'])

        self.client.post(self.base_url, self.product_data)
        self.client.post(self.base_url, self.product_data_2)

        list_response = self.client.get(reverse("product-view"))
        list_response_result = list_response.data['results']

        list_products = [self.product_data, self.product_data_2]

        for index, product in enumerate(list_products):
            for key, item in product.items():
                if key == 'seller_id':
                    self.assertEqual(item, account.id)
                    continue
                    
                if key == 'is_active':
                    self.assertEqual(item, True)
                    continue

                self.assertEqual(item, list_response_result[index][key])
    

    def test_create_product_negative_amount(self):
        print("test create product with negative amount")
        
        product_data_negative_amount = {
            "description": "hyperx microphone",
            "price": 100,
            "quantity": -15
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.seller_token.key)

        response = self.client.post(self.base_url, product_data_negative_amount)

        expected_code = status.HTTP_400_BAD_REQUEST
        expected_message = "Ensure This Value Is Greater Than Or Equal To 0."

        self.assertEqual(response.status_code, expected_code)
        self.assertEqual(response.data["quantity"][0].title(), expected_message)


class TestProductDetailView(APITestCase):
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
            "username": "krun",
            "password": "1234",
            "first_name": "krun",
            "last_name": "demno",
            "is_seller": True
        }

        cls.product_data = {
            "description": "Smartband XYZ 3.22",
            "price": "100.99",
            "quantity": 15
        }

        cls.product_update_data = {
            "description": "updated"
        }

        cls.regular_account = Account.objects.create_user(**cls.account_data_2)
        cls.regular_token = Token.objects.create(user=cls.regular_account)

        cls.seller_account = Account.objects.create_user(**cls.account_data_1)
        cls.seller_token = Token.objects.create(user=cls.seller_account)

        cls.product = Product.objects.create(**cls.product_data, seller_id = cls.seller_account.id)
        cls.detail_url = reverse("product-detail", kwargs={"pk": cls.product.id})
        cls.data_to_update = {"description": "updated"}

    
    def test_product_owner_can_update_product(self):
        print("test product owner can update product")
        
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.seller_token.key)

        response = self.client.patch(self.detail_url, self.data_to_update)

        expected_response = status.HTTP_200_OK

        self.assertEqual(response.status_code, expected_response)
        self.assertEqual(response.data["description"], self.data_to_update["description"])


    def test_non_product_owner_can_not_updated_product(self):
        print("test non product owner can not update product")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.regular_token.key)

        response = self.client.patch(self.detail_url, self.data_to_update)

        excepted_response = status.HTTP_403_FORBIDDEN

        self.assertEqual(response.status_code, excepted_response)
    

  
