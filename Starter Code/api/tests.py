from django.test import TestCase    
from api.models import User, Order
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.
class UserOrderTestCase(TestCase):
    def setUp(self):
        self.user1= User.objects.create_user(username= "user1", password="testcase12")
        self.user2= User.objects.create_user(username="user2", password="testcase12")
        Order.objects.create(user=self.user1)
        Order.objects.create(user=self.user2)
        Order.objects.create(user=self.user2)

    def test_user_retrieved_data_authenticated(self):
        user= User.objects.get(username="user1")
        self.client.force_login(user)
        response= self.client.get(reverse("user-orders"))   

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        orders= response.json()
        self.assertTrue(all(order["user"]== user.id for order in orders))   

    def test_user_order_unauthenticated(self):
        response= self.client.get(reverse("user-orders"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)