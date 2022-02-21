from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from menuapi.models import Menu, Meal

from django.contrib.auth import get_user_model

User = get_user_model()

MENUS_URL_ = 'http://localhost/menus/'
MENUS_URL = '/menus/'
MEALS_URL = '/meals/'
UNAME = 'user'
PASSW = 'password123'


class MenuListTests(APITestCase):

    def setUp(self):
        user = User(username=UNAME, password=PASSW)
        user.save()
        self.user = User.objects.get(username=UNAME)
        self.client.force_authenticate(user=self.user)
        m = Menu(id=123, name='Test1', description='Desc1')
        m.save()

    def test_list_menu(self):
        response = self.client.get('/menus/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MenusTests(APITestCase):

    def setUp(self):
        user = User(username=UNAME, password=PASSW)
        user.save()
        self.user = User.objects.get(username=UNAME)
        self.client.force_authenticate(user=self.user)

    def test_create_menu(self):
        data = {'name': 'TstMenu', 'description': 'Description', 'meals': []}
        response = self.client.post(MENUS_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 1)
        self.assertEqual(Menu.objects.get().name, 'TstMenu')
        self.assertEqual(Menu.objects.get().description, 'Description')
        self.assertEqual(Menu.objects.get().meals.all().count(), 0)

    def test_create_meal(self):
        data = {'name': 'TstMeal', 'description': 'Description',
                'price': 10, 'prep_time': 10}
        response = self.client.post(MEALS_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Meal.objects.count(), 1)
        self.assertEqual(Meal.objects.get().name, 'TstMeal')
        self.assertEqual(Meal.objects.get().description, 'Description')
        self.assertEqual(Meal.objects.get().price, 10)
        self.assertEqual(Meal.objects.get().prep_time, 10)
