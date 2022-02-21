from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q

from unittest.mock import patch

from menuapi.models import Menu, Meal
from menuapi.tasks import get_recipients_for_news, get_new_or_changed_meals, get_recipe_news
import django.core.mail

import random
from datetime import datetime
from dataclasses import dataclass

import menuapi.tasks
from unittest.mock import MagicMock


@dataclass
class UserData:
    login: str
    password: str
    email: str


def generateWord(length=5):
    sequence = random.sample(range(ord('a'), ord('z')), length)
    letters = map(lambda x: chr(x), sequence)
    word = ''.join(letters)
    return word


def generateNameSet(size=3):
    name_set = set()
    # in case there are duplicate names generated
    # generate until required length of result set is reached
    while(len(name_set) < size):
        word = generateWord(6)
        name_set.add(word)
    return name_set


def generateUserList(size=3):
    user_set = list()
    name_set = generateNameSet(size)
    for name in name_set:
        user = UserData(name, name+"pass", name + "@" + "example.com")
        user_set.append(user)
    return user_set


def create_meal(name):
    meal = Meal(name=name,
                description=f'Description of meal "{name}"',
                price=random.randint(3, 100),
                prep_time=random.randint(5, 60),
                #added_on= timezone.now() - timezone.timedelta(days=2),
                is_vegetarian=bool(random.randint(0, 1)))
    return meal


def get_meals_from_before(when=timezone.now()):
    query_added = Q(added_on__lt=when)
    query_modified = Q(modified_on__lt=when)
    return Meal.objects.filter(query_added & query_modified).all()


class TestTasks(TestCase):

    USER_CNT = 5
    STAFF_CNT = 2
    MEAL_CNT = 10
    MENU_CNT = 3
    MOD_MEALS = 4

    def generateUsers(self):
        users = generateUserList(self.USER_CNT + self.STAFF_CNT)
        generated_users = users[0:self.USER_CNT]
        generated_staff = users[self.USER_CNT:]
        for u in generated_users:
            user = User(username=u.login, password=u.password, email=u.email)
            user.save()
        for u in generated_staff:
            user = User(username=u.login, password=u.password,
                        email=u.email, is_staff=True)
            user.save()

    def generateMeals(self):
        #print('generating meals')
        meal_names = generateNameSet(self.MEAL_CNT)
        for name in meal_names:
            meal = create_meal(name)
            meal.save()
        meals = Meal.objects.all()
        #print(f'meal count: {meals.count()}')

    def generateMenus(self):
        meals = Meal.objects.all()
        menu_names = generateNameSet(self.MENU_CNT)
        for name in menu_names:
            menu = Menu(name=name, description=name+"Description")
            menu.save()
            rnd_meals = random.sample(
                list(meals), random.randint(1, len(meals)))
            menu.meals.add(*rnd_meals)
            menu.save()

    def modifyMeals(self):
        #print('modifying meals')
        meals = Meal.objects.all()
        self.mod_meals = random.sample(list(meals), self.MOD_MEALS)
        for meal in self.mod_meals:
            #print(f'modifying: {meal.name}')
            meal.price = 20
            meal.save()

    def setUp(self):
        self.generateUsers()
        self.generateMeals()
        self.generateMenus()

        self.created_time = timezone.now()

        self.modifyMeals()

    def test_get_recipients_save_stuff(self):
        rec = get_recipients_for_news()
        self.assertEqual(len(rec), self.USER_CNT)

    def test_get_recipients_with_stuff(self):
        rec = get_recipients_for_news(inc_staff=True)
        self.assertEqual(len(rec), self.USER_CNT+self.STAFF_CNT)

    def test_gen_new_or_changed_meals(self):
        meals = get_new_or_changed_meals(since=self.created_time)
        self.assertEqual(len(meals), self.MOD_MEALS)

    def test_get_recipe_news_gets_only_modified_or_new_meals(self):
        meals = get_new_or_changed_meals(since=self.created_time)
        old_meals = get_meals_from_before(when=self.created_time)
        news = get_recipe_news(since=self.created_time)
        self.assertEqual(len(meals), self.MOD_MEALS)
        for meal in meals:
            self.assertIn(meal.name, news)
        for meal in old_meals:
            self.assertNotIn(meal.name, news)

    def test_send_email_is_called(self):
        menuapi.tasks.send_email = MagicMock(name='method')

        menuapi.tasks.send_emails()
        menuapi.tasks.send_email.assert_called_once()
