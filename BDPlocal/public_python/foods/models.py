from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Plan(models.Model):
    energy = models.DecimalField(decimal_places=0, max_digits=5)
    protein = models.DecimalField(decimal_places=1, max_digits=5)
    carbohydrate = models.DecimalField(decimal_places=1, max_digits=5)
    fat = models.DecimalField(decimal_places=1, max_digits=5)

class CustomPlan(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    name = models.CharField(max_length=50)

class BasicPlan(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE)

class Food(models.Model):
    name = models.CharField(max_length=80)
    energy = models.DecimalField(max_digits=5, decimal_places=1)
    protein = models.DecimalField(max_digits=5, decimal_places=1)
    fat = models.DecimalField(max_digits=5, decimal_places=1)
    carbohydrate = models.DecimalField(max_digits=5, decimal_places=1)

class FoundationFood(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=False)

class CustomFood(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

class FoodSet(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)

class Component(models.Model):
    food_set_id = models.ForeignKey(FoodSet, on_delete=models.CASCADE)
    food_id = models.ForeignKey(Food, on_delete=models.CASCADE)
    weight = models.DecimalField(decimal_places=1, max_digits=5)

class Meal(models.Model):
    food_set_id = models.ForeignKey(FoodSet, on_delete=models.CASCADE)
    date_of_eating = models.DateField()

class Recipe(models.Model):
    food_set_id = models.ForeignKey(FoodSet, on_delete=models.CASCADE)

class ShoppingList(models.Model):
    food_set_id = models.ForeignKey(FoodSet, on_delete=models.CASCADE)


