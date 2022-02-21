from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from menuapi import views



urlpatterns = [
    path('meals/', views.MealList.as_view()),
    path('meals/<int:pk>/', views.MealDetail.as_view()),
    path('menus/', views.MenuList.as_view()),
    path('menus/<int:pk>/', views.MenuDetail.as_view()),
    path('view/menus/<int:pk>/', views.MenuMealDetail.as_view()),
    path('view/menus/', views.MenuMealList.as_view()),
    path('', views.index),
]

urlpatterns = format_suffix_patterns(urlpatterns)
