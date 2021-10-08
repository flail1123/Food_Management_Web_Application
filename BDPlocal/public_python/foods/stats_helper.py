from .models import *
from datetime import date
import datetime
from .calendar_helper import *
from django.db.models import Q

def month_symbol(nr):
    return ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII'][nr - 1]

def date_label(day: date):
    return str(day.day) + ' ' + month_symbol(day.month)

def date_label_set_string(first_day: date, last_day: date):
    result = []
    while first_day <= last_day:
        result.append(date_label(first_day))
        first_day += datetime.timedelta(days=1)
    return result

def energy_sum_for_day(request, day: date):
    result = 0
    day_meals = Meal.objects.filter(date_of_eating=day, food_set_id__user_id=request.user.id)
    for meal in day_meals:
        result += get_calories_sum_for_meal(meal.food_set_id.id)
    return result

def energy_set_string(request, first_day: date, last_day: date):
    result = []
    while first_day <= last_day:
        result.append(energy_sum_for_day(request, first_day))
        first_day += datetime.timedelta(days=1)
    return result

def protein_sum_for_day(request, day: date):
    result = 0
    day_meals = Meal.objects.filter(date_of_eating=day, food_set_id__user_id=request.user.id)
    for meal in day_meals:
        result += get_protein_sum_for_meal(meal.food_set_id.id)
    return result

def protein_set_string(request, first_day: date, last_day: date):
    result = []
    while first_day <= last_day:
        result.append(protein_sum_for_day(request, first_day))
        first_day += datetime.timedelta(days=1)
    return result

def carbohydrate_sum_for_day(request, day: date):
    result = 0
    day_meals = Meal.objects.filter(date_of_eating=day, food_set_id__user_id=request.user.id)
    for meal in day_meals:
        result += get_carbohydrate_sum_for_meal(meal.food_set_id.id)
    return result

def carbohydrate_set_string(request, first_day: date, last_day: date):
    result = []
    while first_day <= last_day:
        result.append(carbohydrate_sum_for_day(request, first_day))
        first_day += datetime.timedelta(days=1)
    return result

def fat_sum_for_day(request, day: date):
    result = 0
    day_meals = Meal.objects.filter(date_of_eating=day, food_set_id__user_id=request.user.id)
    for meal in day_meals:
        result += get_fat_sum_for_meal(meal.food_set_id.id)
    return result

def fat_set_string(request, first_day: date, last_day: date):
    result = []
    while first_day <= last_day:
        result.append(fat_sum_for_day(request, first_day))
        first_day += datetime.timedelta(days=1)
    return result

def planToDisplay(request, displayedDate):
    customs = CustomPlan.objects.filter(user_id=request.user.id, start_date__lte=displayedDate, end_date__gte=displayedDate)
    if customs:
        customFilter = Q()
        for custom in customs:
            customFilter = customFilter | Q(id=custom.plan_id.id)
        anyValidCustom = Plan.objects.filter(customFilter)
        if anyValidCustom:
            return anyValidCustom[0]
    isBasic = BasicPlan.objects.filter(user_id_id__id=request.user.id)
    if isBasic:
        return isBasic[0].plan_id
    return False

def planned_energy_for_day(request, day):
    plan = planToDisplay(request, day)
    if plan:
        return int(plan.energy)
    else:
        return 0

def planned_energy_for_period(request, start_date: date, end_date: date):
    result = []
    while start_date <= end_date:
        result.append(planned_energy_for_day(request, start_date))
        start_date += datetime.timedelta(days=1)
    return result

def planned_protein_for_day(request, day):
    plan = planToDisplay(request, day)
    if plan:
        return int(plan.protein)
    else:
        return 0

def planned_protein_for_period(request, start_date: date, end_date: date):
    result = []
    while start_date <= end_date:
        result.append(planned_protein_for_day(request, start_date))
        start_date += datetime.timedelta(days=1)
    return result

def planned_carbohydrate_for_day(request, day):
    plan = planToDisplay(request, day)
    if plan:
        return int(plan.carbohydrate)
    else:
        return 0

def planned_carbohydrate_for_period(request, start_date: date, end_date: date):
    result = []
    while start_date <= end_date:
        result.append(planned_carbohydrate_for_day(request, start_date))
        start_date += datetime.timedelta(days=1)
    return result

def planned_fat_for_day(request, day):
    plan = planToDisplay(request, day)
    if plan:
        return int(plan.fat)
    else:
        return 0

def planned_fat_for_period(request, start_date: date, end_date: date):
    result = []
    while start_date <= end_date:
        result.append(planned_fat_for_day(request, start_date))
        start_date += datetime.timedelta(days=1)
    return result





