from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('products/', views.products, name='products'),
    path('calendar/', views.calendar, name='calendar'),
    path('plans/', views.plans, name='plans'),
    path('lists/', views.lists, name='lists'),
    path('recipes/', views.recipes, name='recipes'),
    path('meals/', views.meals, name='meals'),
    path('stats/', views.stats, name='stats'),
    path('logout/', views.logout, name='logout'),
    path('', views.home, name='home')
]

