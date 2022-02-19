from rest_framework import serializers
from menuapi.models import Menu, Meal

class MealSerializer(serializers.ModelSerializer):
    #id = serializers.IntegerField(read_only=True)
    class Meta: 
        model = Meal
        fields = '__all__'
        read_only_fields = ['added_on', 'modified_on']
        # fields = ['name', 'description', 'price', 'prep_time', 'added_on', 'modified_on', 'is_vegetarian']
    
class MenuSerializer(serializers.ModelSerializer):
    #id = serializers.IntegerField(read_only=True)
    class Meta: 
        model = Menu
        fields = '__all__'
        read_only_fields = ['added_on', 'modified_on', 'meal_count']
        # depth = 1
    

class MenuMealSerializer(serializers.ModelSerializer):
    #id = serializers.IntegerField(read_only=True)
    class Meta: 
        model = Menu
        fields = '__all__'
        read_only_fields = ['added_on', 'modified_on', 'meal_count', 'name', 'description','meals']
        depth = 1