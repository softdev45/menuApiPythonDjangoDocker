from django.shortcuts import render

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect

from menuapi.models import Menu, Meal
from menuapi.serializers import MealSerializer, MenuSerializer, MenuMealSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, mixins
from rest_framework import permissions
from rest_framework import filters

from django_filters import rest_framework as django_filters

# Create your views here.

# class MealList(APIView):
#     """
#     List all meals, or create a new meal.
#     """
#     def get(self, request, format=None):
#         meals = Meal.objects.all()
#         serializer = MealSerializer(meals, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = MealSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class MealDetail(APIView):
#     """
#     Retrieve, update or delete a meal instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Meal.objects.get(pk=pk)
#         except Meal.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         meal = self.get_object(pk)
#         serializer = MealSerializer(meal)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         meal = self.get_object(pk)
#         serializer = MealSerializer(meal, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         meal = self.get_object(pk)
#         meal.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/menu')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

class MealList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    


class MealDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Meal.objects.all()
    serializer_class = MealSerializer



class MenuFilter(django_filters.FilterSet):

    added_on = django_filters.DateTimeFilter(field_name='added_on')
    added_on__gt = django_filters.DateTimeFilter(field_name='added_on', lookup_expr='gt')
    added_on__lt = django_filters.DateTimeFilter(field_name='added_on', lookup_expr='lt')

    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Menu
        fields ={'modified_on' : ['lt', 'gt'] }


class MenuList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Menu.objects.filter(meal_count__gt=0).all()
    serializer_class = MenuSerializer
    filter_backends = (filters.OrderingFilter,django_filters.DjangoFilterBackend)
    ordering_fields = ['name', 'meal_count']
    filterset_class = MenuFilter

    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)

class MenuMealDetail( generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Menu.objects.all()
    serializer_class = MenuMealSerializer


class MenuDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
