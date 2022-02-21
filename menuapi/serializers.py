from rest_framework import serializers
from menuapi.models import Menu, Meal


class MealSerializer(serializers.ModelSerializer):
    """ Class to serialize Meals """
    class Meta:
        model = Meal
        fields = '__all__'
        read_only_fields = ['added_on', 'modified_on']


class MenuSerializer(serializers.ModelSerializer):
    """ Class to serialize Meanus """
    class Meta:
        model = Menu
        fields = '__all__'
        read_only_fields = ['added_on', 'modified_on', 'meal_count']


class MenuMealSerializer(serializers.ModelSerializer):
    """ Class to Serialize Menus with Meals together """
    class Meta:
        model = Menu
        fields = '__all__'
        read_only_fields = ['added_on', 'modified_on',
                            'meal_count', 'name', 'description', 'meals']
        depth = 1
