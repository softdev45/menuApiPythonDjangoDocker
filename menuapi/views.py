from django.shortcuts import render

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.http import Http404

from menuapi.models import Menu, Meal
from menuapi.forms import SignUpForm
from menuapi.serializers import MealSerializer, MenuSerializer, MenuMealSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, mixins
from rest_framework import permissions
from rest_framework import filters

from django_filters import rest_framework as django_filters

import logging

logger = logging.getLogger(__name__)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/menu')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def index(request):
    return render(request, 'index.html')


class MealFilter(django_filters.FilterSet):

    added_on__date = django_filters.DateTimeFilter(field_name='added_on', lookup_expr='date')
    added_on__gt = django_filters.DateTimeFilter(field_name='added_on', lookup_expr='gt')
    added_on__lt = django_filters.DateTimeFilter(field_name='added_on', lookup_expr='lt')

    modified_on__date = django_filters.DateTimeFilter(field_name='modified_on', lookup_expr='date')
    modified_on__gt = django_filters.DateTimeFilter(field_name='modified_on', lookup_expr='gt')
    modified_on__lt = django_filters.DateTimeFilter(field_name='modified_on', lookup_expr='lt')

    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Meal
        fields ={'modified_on' : ['lt', 'gt'] }


class MealList(generics.ListCreateAPIView):
    """ List all meals with ordering and filters """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    filter_backends = (filters.OrderingFilter,django_filters.DjangoFilterBackend)
    ordering_fields = ['name']
    filterset_class = MealFilter
    


class MealDetail(generics.RetrieveUpdateDestroyAPIView):
    """ View selected Meal and update or delete it """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

class MenuFilter(django_filters.FilterSet):

    added_on__date = django_filters.DateTimeFilter(field_name='added_on', lookup_expr='date')
    added_on__gt = django_filters.DateTimeFilter(field_name='added_on', lookup_expr='gt')
    added_on__lt = django_filters.DateTimeFilter(field_name='added_on', lookup_expr='lt')

    modified_on__date = django_filters.DateTimeFilter(field_name='modified_on', lookup_expr='date')
    modified_on__gt = django_filters.DateTimeFilter(field_name='modified_on', lookup_expr='gt')
    modified_on__lt = django_filters.DateTimeFilter(field_name='modified_on', lookup_expr='lt')

    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Menu
        fields ={'modified_on' : ['lt', 'gt'] }


class MenuList(generics.ListCreateAPIView):
    """ List Menus """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Menu.objects.filter(meal_count__gt=0).all()
    serializer_class = MenuSerializer
    filter_backends = (filters.OrderingFilter,django_filters.DjangoFilterBackend)
    ordering_fields = ['name', 'meal_count']
    filterset_class = MenuFilter

class MenuDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Get Update or Delete Menu """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class MenuMealDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """ View single Menus with Meals objects included """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Menu.objects.all()
    serializer_class = MenuMealSerializer

    def get(self, request, *args, **kwargs):        
        logger.info(f'Getting detailed view: {request},{args},{kwargs}')
        return self.retrieve(request, *args, **kwargs)

class MenuMealList(mixins.ListModelMixin, generics.GenericAPIView):
    """ View Menus with Meals objects included """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Menu.objects.all()
    serializer_class = MenuMealSerializer

    def get(self, request, *args, **kwargs):        
        logger.info(f'Getting List view: {request},{args},{kwargs}')
        return self.list(request, *args, **kwargs)

