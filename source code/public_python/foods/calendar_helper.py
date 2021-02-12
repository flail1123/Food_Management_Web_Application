from .models import *
from datetime import date

def get_calories_sum_for_meal(meal_id):
    all_components = Component.objects.filter(food_set_id__id=meal_id)
    result = 0
    for component in all_components:
        result += component.food_id.energy * component.weight / 100
    return result

def get_protein_sum_for_meal(meal_id):
    all_components = Component.objects.filter(food_set_id__id=meal_id)
    result = 0
    for component in all_components:
        result += component.food_id.protein * component.weight / 100
    return result

def get_carbohydrate_sum_for_meal(meal_id):
    all_components = Component.objects.filter(food_set_id__id=meal_id)
    result = 0
    for component in all_components:
        result += component.food_id.carbohydrate * component.weight / 100
    return result

def get_fat_sum_for_meal(meal_id):
    all_components = Component.objects.filter(food_set_id__id=meal_id)
    result = 0
    for component in all_components:
        result += component.food_id.fat * component.weight / 100
    return result

def meals_list(request, day):
    meals = Meal.objects.filter(date_of_eating=day, food_set_id__user_id=request.user.id)
    result = []
    sums = {'energy': 0, 'protein': 0, 'carbohydrate': 0, 'fat': 0}
    for meal in meals:
        current_meal = {}
        current_meal['name'] = meal.food_set_id.name
        current_meal['id'] = meal.food_set_id.id
        current_meal['energy'] = get_calories_sum_for_meal(current_meal['id'])
        sums['energy'] += current_meal['energy']
        current_meal['energy'] = int(current_meal['energy'])
        current_meal['protein'] = get_protein_sum_for_meal(current_meal['id'])
        sums['protein'] += current_meal['protein']
        current_meal['carbohydrate'] = get_carbohydrate_sum_for_meal(current_meal['id'])
        sums['carbohydrate'] += current_meal['carbohydrate']
        current_meal['fat'] = get_fat_sum_for_meal(current_meal['id'])
        sums['fat'] += current_meal['fat']
        result.append(current_meal)
        sums['energy'] = int(sums['energy'])
        sums['protein'] = int(sums['protein'])
        sums['carbohydrate'] = int(sums['carbohydrate'])
        sums['fat'] = int(sums['fat'])
    return {'meals': result, 'sums': sums}

