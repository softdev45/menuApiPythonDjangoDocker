from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from django.db.models.signals import m2m_changed
from django.core.validators import MinValueValidator
from decimal import Decimal


class Meal(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=6, validators=[
                                MinValueValidator(Decimal('0.01'))])
    prep_time = models.PositiveIntegerField()
    added_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    is_vegetarian = models.BooleanField(default=False)


class Menu(models.Model):
    name = models.CharField(max_length=100, blank=True,
                            default='', unique=True)
    description = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    meals = models.ManyToManyField(Meal, related_name='menus', blank=True)
    meal_count = models.PositiveIntegerField(default=0, blank=True, null=True)


@receiver(m2m_changed, sender=Menu.meals.through)
def meals_changed(sender, action, pk_set, instance=None, **kwargs):
    if action in ['post_add', 'post_remove']:
        instance.meal_count = instance.meals.count()
        instance.save()
