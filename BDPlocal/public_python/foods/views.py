from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.db.models import Q
from .models import *
from datetime import date
import datetime
from .calendar_helper import *
from .stats_helper import *

# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return render(request, 'register.html', {'mess': 'PASSWORDS MUST MATCH'})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'mess': 'USERNAME ALREADY EXISTS'})

        user = User.objects.create_user(username=username, password=password1, email=email)
        user.save()

        return redirect('/login', {'succ': 'ACCOUNT CREATED'})

    return render(request, 'register.html')

def home(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    return redirect('/calendar')

def get_foundation_products(request, search=''):
    injected_search = '%' + search.lower() + '%'
    result = FoundationFood.objects.raw('SELECT * FROM foods_foundationfood LEFT JOIN foods_food ON foods_foundationfood.food_id = foods_food.id WHERE LOWER(foods_food.name) LIKE %s ORDER BY LENGTH(foods_food.name) ASC', [injected_search])
    return result[:100]

def get_custom_products(request, search=''):
    injected_search = '%' + search.lower() + '%'
    result = FoundationFood.objects.raw('SELECT * FROM foods_customfood LEFT JOIN foods_food ON foods_customfood.food_id = foods_food.id WHERE LOWER(foods_food.name) LIKE %s AND foods_customfood.user_id=%s ORDER BY LENGTH(foods_food.name) ASC', [injected_search, request.user.id])
    return result[:100]

def products(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    searchtext = request.GET.get('searchtext', '')
    check_only_customs = True if request.GET.get('searchonlycustom') else False
    foundation_products = get_foundation_products(request, searchtext) if not check_only_customs else []
    custom_products = get_custom_products(request, searchtext)
    return render(request, 'products.html', {'custom_products': custom_products, 'foundation_products': foundation_products, 'only_custom': check_only_customs})

def is_any_custom_food_with_user_id_and_name(user_id, name):
    found_products = CustomFood.objects.raw('SELECT * FROM foods_customfood LEFT JOIN foods_food ON foods_customfood.food_id = foods_food.id WHERE foods_customfood.user_id=%s AND foods_food.name=%s', [user_id, name])
    return len(found_products) > 0

# zwraca napis z wiadomością, jeśli jest błąd (czyli true); wpp. zwraca pusty string (czyli false)
def validate_new_product(request, properties):
    if not properties['name'] and properties['energy'] and properties['protein'] and properties['fat'] and properties['carb']:
        return 'Please fill all fields'
    try:
        properties['energy'] = float(properties['energy'])
        properties['protein'] = float(properties['protein'])
        properties['fat'] = float(properties['fat'])
        properties['carb'] = float(properties['carb'])
    except ValueError:
        return 'Calories, proteins, fats, carbohydrates must be integers or decimal numbers'
    if len(properties['name']) > 80:
        return 'Product name length cannot exceed 80 characters'
    if properties['energy'] > 1000:
        return 'Calories cannot exceed 1000'
    if properties['protein'] + properties['fat'] + properties['carb'] > 100:
        return 'Proteins, fats and carbohydrates cannot sum up to more than 100'
    if properties['energy'] < 0 or properties['protein'] < 0 or properties['fat'] < 0 or properties['carb'] < 0:
        return 'You must provide non-negative values'
    if is_any_custom_food_with_user_id_and_name(request.user.id, properties['name']):
        return 'You already created custom product with this name'
    # wszystko ok
    return ''
    

def handle_creating_new_product(request):
    properties = {}
    properties['name'] = request.POST['name']
    properties['energy'] = request.POST['energy'].replace(',', '.')
    properties['protein'] = request.POST['protein'].replace(',', '.')
    properties['fat'] = request.POST['fat'].replace(',', '.')
    properties['carb'] = request.POST['carb'].replace(',', '.')
    validate_message = validate_new_product(request, properties)
    if validate_message:
        return render(request, 'createproduct.html', {'mess': validate_message, 'details': properties})
    new_product = Food(name=properties['name'], energy=properties['energy'], protein=properties['protein'], fat=properties['fat'], carbohydrate=properties['carb'])
    new_product.save()
    new_custom_product = CustomFood(user=request.user, food=new_product)
    new_custom_product.save()
    return render(request, 'productcreated.html', {'message': 'Product created', 'another': True})
    
def createproduct(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'POST':
        return handle_creating_new_product(request)
    else:
        return render(request, 'createproduct.html')

    
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
        basicFilter = Q()
        basicFilter = basicFilter | Q(id=isBasic[0].plan_id)
        basics = Plan.objects.filter(basicFilter)
        return basics[0]
    return False


def createDateInfo(request):
    if request.method == 'POST':
        displayedDate = date(year=int(request.POST['year']), month=int(request.POST['month']), day=int(request.POST['day']))
    else:
        displayedDate = date.today()
    dateString = f'{str(displayedDate.strftime("%d"))} {displayedDate.strftime("%b")} {displayedDate.strftime("%Y")}'
    dateInfo = {}
    dateInfo['date'] = displayedDate
    dateInfo['dateString'] = dateString.lstrip('0')
    dateInfo['day'] = displayedDate.day
    dateInfo['month'] = displayedDate.month
    dateInfo['year'] = displayedDate.year
    dateInfo['displayedDate'] = displayedDate
    return dateInfo

def calendar(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    dateInfo = createDateInfo(request)
    meals_data = meals_list(request, dateInfo['date'])
    displayedPlan = planToDisplay(request, dateInfo['displayedDate'])
    planInfo = {}
    if displayedPlan:
        planInfo['energy'] = int(displayedPlan.energy)
        planInfo['proteins'] = int(displayedPlan.protein)
        planInfo['fats'] = int(displayedPlan.fat)
        planInfo['carbs'] = int(displayedPlan.carbohydrate)
        return render(request, 'calendar.html', {'anyPlan': True, 'planInfo': planInfo, 'dateInfo': dateInfo, 'meals': meals_data['meals'], 'sums': meals_data['sums']})
    else:
        return render(request, 'calendar.html', {'anyPlan': False, 'dateInfo': dateInfo, 'meals': meals_data['meals'], 'sums': meals_data['sums']})
    return redirect(request, 'meals.html')

def plans(request, displayedPlanId=-1, deleteId=-1):
    displayedPlanId = int(displayedPlanId)
    deleteId = int(deleteId)
    if deleteId != -1:
        displayedPlanId = -1
        CustomPlan.objects.filter(id=deleteId).delete()
    if not request.user.is_authenticated:
        return redirect('/login')
    try:
        search = request.GET['planName']
    except:
        search = ""

    plans = []
    user = request.user
    for customPlan in CustomPlan.objects.all():
        if customPlan.user_id == user and search in customPlan.name:
            plans.append(customPlan)
    # print(plans)
    if displayedPlanId == -1:
        displayedCustomPlan = -1

        for basicPlan in BasicPlan.objects.all():
            if basicPlan.user_id == user:
                displayedCustomPlan = basicPlan
        if displayedCustomPlan != -1:
            for plan in Plan.objects.all():
                if plan == displayedCustomPlan.plan_id:
                    displayedPlan = plan
        else:
            displayedPlan = -1
        displayedCustomPlan = -1
    else:
        displayedCustomPlan = CustomPlan.objects.get(id=displayedPlanId);
        for plan in Plan.objects.all():
            if plan == displayedCustomPlan.plan_id:
                displayedPlan = plan
    return render(request, 'plans.html',
                  {"displayedPlan": displayedPlan, "displayedCustomPlan": displayedCustomPlan, "plans": plans})


def editBasicPlan(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    try:
        planOfBasicPlan = BasicPlan.objects.filter(user_id=request.user).get().plan_id
    except:
        planOfBasicPlan = -1

    if request.method == 'POST':
        energy = request.POST['energy']
        protein = request.POST['protein']
        fat = request.POST['fat']
        carb = request.POST['carb']

        try:
            energy = float(energy)
            protein = float(protein)
            fat = float(fat)
            carb = float(carb)
        except ValueError:
            return render(request, 'edit_basic_plan.html',
                          {'mess': 'Calories, proteins, fats, carbohydrates must be integers or decimal numbers',
                           "plan": planOfBasicPlan})

        if energy > 99999 or protein > 9999.9 or fat > 9999.9 or carb > 9999.9:
            return render(request, 'edit_basic_plan.html',
                          {'mess': 'Value limit exceeded', "plan": planOfBasicPlan})

        if energy < 0 or protein < 0 or fat < 0 or carb < 0:
            return render(request, 'edit_basic_plan.html',
                          {'mess': 'You must provide positive values', "plan": planOfBasicPlan})
        user = request.user
        try:
            BasicPlan.objects.filter(user_id=user).delete()
        except:
            pass

        newPlan = Plan(energy=energy, protein=protein, fat=fat, carbohydrate=carb)
        newPlan.save()
        newBasicPlan = BasicPlan(user_id=user, plan_id=newPlan)
        newBasicPlan.save()
        return render(request, 'plan_edited.html')
    else:

        return render(request, 'edit_basic_plan.html', {"plan": planOfBasicPlan})


def createPlan(request, planId=-1, edit=0):
    if not request.user.is_authenticated:
        return redirect('/login')
    edit = int(edit)
    planId = int(planId)
    if planId != -1:
        displayedCustomPlan = CustomPlan.objects.get(id=planId)
        displayedPlan = displayedCustomPlan.plan_id
        startDate = displayedCustomPlan.start_date.strftime("%Y-%m-%d")
        endDate = displayedCustomPlan.end_date.strftime("%Y-%m-%d")
    else:
        displayedCustomPlan = -1
        displayedPlan = -1
        startDate = -1
        endDate = -1


    dict = {"planId": planId, "edit": edit, "displayedPlan": displayedPlan, "displayedCustomPlan": displayedCustomPlan,
            "endDate": endDate, "startDate": startDate}

    if request.method == 'POST':
        name = request.POST['name']
        energy = request.POST['energy']
        protein = request.POST['protein']
        fat = request.POST['fat']
        carb = request.POST['carb']
        startDate = request.POST['startDate']
        print('SD:', startDate)
        endDate = request.POST['endDate']
        print('ED:', endDate)

        if startDate == '' or endDate == '':
            dict['mess'] = 'Not valid dates'
            return render(request, 'create_plan.html', dict)

        startDate = datetime.datetime.strptime(startDate, "%Y-%m-%d")
        endDate = datetime.datetime.strptime(endDate, "%Y-%m-%d")

        try:
            energy = float(energy)
            protein = float(protein)
            fat = float(fat)
            carb = float(carb)
        except ValueError:
            dict['mess'] = 'Calories, proteins, fats, carbohydrates must be integers or decimal numbers'
            return render(request, 'create_plan.html', dict)

        if startDate > endDate:
            dict['mess'] = 'Start date has to be a date before end date'
            return render(request, 'create_plan.html', dict)
        if energy > 99999:
            dict['mess'] = 'Calories cannot exceed 99999'
            return render(request, 'create_plan.html', dict)
        if energy < 0 or protein < 0 or fat < 0 or carb < 0:
            dict['mess'] = 'You must provide positive values'
            return render(request, 'create_plan.html', dict)
        user = request.user
        table =[]
        table += FoundationFood.objects.raw('SELECT * FROM foods_customplan WHERE user_id_id = %s and start_date <= %s and end_date >= %s', [user.id, endDate, startDate])
        print(table)
        if len(table) > edit:
            dict['mess'] = "Plan's dates can't overlaps"
            return render(request, 'create_plan.html', dict)


        print("edit: ", edit)
        if CustomPlan.objects.filter(user_id=user).filter(name=name).count() > edit:
            dict['mess'] = 'You already created product with that name'
            return render(request, 'create_plan.html', dict)
        if edit:
            CustomPlan.objects.filter(id=planId).delete()
        newPlan = Plan(energy=energy, protein=protein, fat=fat, carbohydrate=carb)
        newPlan.save()
        newCustomPlan = CustomPlan(user_id=user, plan_id=newPlan, start_date=startDate, end_date=endDate, name=name)
        newCustomPlan.save()
        if edit:
            return render(request, 'plan_edited.html')
        else:
            return render(request, 'plan_created.html')
    else:
        return render(request, 'create_plan.html', dict)

def foodSets(request, foodSetKind, deleteId):
    if not request.user.is_authenticated:
        return redirect('/login')
    try:
        search = request.GET['name']
    except:
        search = ""
    user = request.user
    if (deleteId != -1):
        FoodSet.objects.filter(id=deleteId).delete()
    injected_search = '%' + search.lower() + '%'
    foodSetsInfo = []
    if foodSetKind == 'meals':
        table = FoundationFood.objects.raw('SELECT foods_foodset.id as id, date_of_eating, name FROM foods_meal LEFT JOIN foods_foodset ON foods_foodset.id = foods_meal.food_set_id_id WHERE foods_foodset.user_id_id = %s and LOWER(name) LIKE %s LIMIT 100', [user.id, injected_search])
        for record in table:
            foodSetsInfo.append((record.date_of_eating, record.name, record.id))
    elif foodSetKind == 'shoppingLists':
        table = FoundationFood.objects.raw('SELECT foods_foodset.id as id, name FROM foods_shoppinglist LEFT JOIN foods_foodset ON foods_foodset.id = foods_shoppinglist.food_set_id_id WHERE foods_foodset.user_id_id = %s and LOWER(name) LIKE %s LIMIT 100', [user.id, injected_search])
        for record in table:
            foodSetsInfo.append((record.name, record.id))
    else:
        table = FoundationFood.objects.raw('SELECT foods_foodset.id as id, name FROM foods_recipe LEFT JOIN foods_foodset ON foods_foodset.id = foods_recipe.food_set_id_id WHERE foods_foodset.user_id_id = %s and LOWER(name) LIKE %s LIMIT 100', [user.id, injected_search])
        for record in table:
            foodSetsInfo.append((record.name, record.id))


    return render(request, 'list_food_sets.html', {"list": foodSetsInfo, "foodSetKind": foodSetKind})

def lists(request, deleteId=-1):
    return foodSets(request, "shoppingLists", int(deleteId))


def recipes(request, deleteId=-1):
    return foodSets(request, "recipes", int(deleteId))

def addProductToFoodSet(request, foodSetKind, foodSetId, productId=-1, mess=""):
    if not request.user.is_authenticated:
        return redirect('/login')
    if not(foodSetKind in ["meals", "shoppingLists", "recipes"]):
        raise Http404
    foodSet = FoodSet.objects.get(id=foodSetId)
    search = request.GET.get('searchtext', '')

    if productId != -1:
        weight = float(request.GET.get('weight'))
        if weight > 9999:
            return addProductToFoodSet(request, foodSetKind, foodSetId, -1, "Weight can't exceed 9999 grams")
        Component.objects.create(weight=weight, food_set_id=foodSet, food_id=Food.objects.get(id=productId))

    check_only_customs = True if request.GET.get('searchonlycustom') else False
    products = []
    injected_search = '%' + search.lower() + '%'
    print(injected_search)
    if not check_only_customs:
        products += FoundationFood.objects.raw(
            'SELECT id, name, energy, protein, fat, carbohydrate FROM (SELECT food.id as id, name, energy, protein, fat, carbohydrate, food_id_id as czy FROM (SELECT foods_food.id as id, name, energy, protein, fat, carbohydrate FROM foods_foundationfood LEFT JOIN foods_food ON foods_foundationfood.food_id = foods_food.id) as food LEFT JOIN foods_component ON food.id = foods_component.food_id_id and %s = foods_component.food_set_id_id) as t WHERE czy is null AND LOWER(name) LIKE %s ORDER BY LENGTH(name) ASC  LIMIT 100',
            [foodSetId, injected_search])

    products += FoundationFood.objects.raw(
    'SELECT id, name, energy, protein, fat, carbohydrate FROM (SELECT food.id as id, name, energy, protein, fat, carbohydrate, food_id_id as czy FROM (SELECT foods_food.id as id, name, energy, protein, fat, carbohydrate FROM foods_customfood LEFT JOIN foods_food ON foods_customfood.food_id = foods_food.id and foods_customfood.user_id = %s) as food LEFT JOIN foods_component ON food.id = foods_component.food_id_id and %s = foods_component.food_set_id_id) as t WHERE czy is null  AND lOWER(name) LIKE %s ORDER BY LENGTH(name) ASC LIMIT 100',
    [request.user.id, foodSetId, injected_search])


    return render(request, 'add_products_to_food_set.html', {'foodSetKind' : foodSetKind,
    'products': products, 'only_custom': check_only_customs, 'foodSetId': foodSetId, 'mess': mess})


def displayFoodSet(request, foodSetKind, foodSetId=-1, deleteId=-1):
    if not(foodSetKind in ["meals", "shoppingLists", "recipes"]):
        raise Http404
    if deleteId != -1:
        Component.objects.filter(id=deleteId).delete()
    foodSet = -1
    if foodSetId != -1:
        foodSet = FoodSet.objects.get(id=foodSetId)

    components = []

    for component in FoundationFood.objects.raw('SELECT * FROM foods_component WHERE foods_component.food_set_id_id = %s', [foodSetId]):
            product = Food.objects.get(id=component.food_id_id)
            percentage = component.weight / 100
            components.append((component, product.name, round(percentage * product.energy, 0), round(percentage * product.fat, 1), round(percentage * product.protein, 1), round(percentage * product.carbohydrate, 1)))
    date = -2
    if foodSetKind == "meals":
        for meal in Meal.objects.all():
            if meal.food_set_id == foodSet:
                date = meal.date_of_eating
    return render(request, 'food_set_display.html', {"foodSet": foodSet, "foodSetKind": foodSetKind, "components":components, "date":date})


def generateShoppingList(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    if request.method == 'POST':
        name = request.POST['name']
        startDate = request.POST['startDate']
        endDate = request.POST['endDate']
        if startDate == '' or endDate == '':
            return render(request, 'generate_shopping_list.html', {"mess":'Fill up all fields'})

        user = request.user
        sameNameList = []
        sameNameList += CustomFood.objects.raw(
            'SELECT foods_foodset.id as id FROM foods_shoppinglist, foods_foodset WHERE food_set_id_id = foods_foodset.id AND user_id_id = %s AND LOWER(name)=%s',
            [user.id, name.lower()])
        if len( sameNameList) > 0:
            return render(request, 'generate_shopping_list.html', {"mess":'You already created shopping list with that name'})

        if startDate > endDate:
            return render(request, 'generate_shopping_list.html',{"mess": 'Start date has to be a date before end date'})

        newFoodSet = FoodSet(user_id=user, name=name)
        newFoodSet.save()
        newObject = ShoppingList(food_set_id=newFoodSet)
        newObject.save()
        products = CustomFood.objects.raw(
            'WITH food_set_ids AS (SELECT DISTINCT foods_foodset.id as id FROM foods_meal, foods_foodset WHERE date_of_eating >= %s AND date_of_eating <= %s AND user_id_id = %s AND foods_foodset.id = foods_meal.food_set_id_id) SELECT food_id_id as id, sum(weight) as weight FROM food_set_ids, foods_component WHERE food_set_ids.id = food_set_id_id  GROUP BY food_id_id',
            [startDate, endDate, user.id])

        for record in products:
            print(record.id, record.weight)
            Component.objects.create(weight=record.weight, food_set_id=newFoodSet, food_id=Food.objects.get(id=record.id))


        return displayFoodSet(request, 'shoppingLists', newFoodSet.id, -1)
    else:
        return render(request, 'generate_shopping_list.html', {'mess': ""})


def createFoodSet(request, foodSetKind, foodSetId=-1, edit=0):
    if not request.user.is_authenticated:
        return redirect('/login')
    edit = int(edit)
    foodSetId = int(foodSetId)
    foodSetKind = str(foodSetKind)
    if not(foodSetKind in ["meals", "shoppingLists", "recipes"]):
        raise Http404
    if foodSetId != -1:
        foodSet = FoodSet.objects.filter(id=foodSetId)
    else:
        foodSet = -1

    if request.method == 'POST':
        name = request.POST['name']
        if foodSetKind == "meals":
            dateOfEating = request.POST['dateOfEating']
        user = request.user
        sameNameList = []
        if foodSetKind == 'meals':
            sameNameList += CustomFood.objects.raw(
                'SELECT foods_foodset.id as id FROM foods_meal, foods_foodset WHERE food_set_id_id = foods_foodset.id AND user_id_id = %s AND LOWER(name)=%s AND date_of_eating = %s',
                [user.id, name.lower(), dateOfEating])
        elif foodSetKind == 'shoppingLists':
            sameNameList += CustomFood.objects.raw(
                'SELECT foods_foodset.id as id FROM foods_shoppinglist, foods_foodset WHERE food_set_id_id = foods_foodset.id AND user_id_id = %s AND LOWER(name)=%s',
                [user.id, name.lower()])
        else:
            sameNameList += CustomFood.objects.raw(
                'SELECT foods_foodset.id as id FROM foods_recipe, foods_foodset WHERE food_set_id_id = foods_foodset.id AND user_id_id = %s AND LOWER(name)=%s',
                [user.id, name.lower()])
        if len( sameNameList)> edit:
            if foodSetKind == 'meals':
                pom = 'meal'
            elif foodSetKind == 'shoppingLists':
                pom = 'shopping list'
            else:
                pom = 'recipe'
            dict = {'mess': 'You already created ' + pom +' with that name', "foodSetId": foodSetId, "edit": edit,
             "foodSetKind": foodSetKind, "date": -1}
            if foodSetKind == "meals" and foodSet != -1:
                for meal in Meal.objects.all():
                    if meal.food_set_id == foodSet:
                        dict["date"] = meal.date_of_eating.strftime("%Y-%m-%d")
            return render(request, 'create_food_set.html',
                          dict)
        if edit:
            foodSet.delete()

        newFoodSet = FoodSet(user_id=user, name=name)
        newFoodSet.save()
        if foodSetKind == "meals":
            newObject = Meal(food_set_id=newFoodSet, date_of_eating=dateOfEating)
        elif foodSetKind == "recipes":
            newObject = Recipe(food_set_id=newFoodSet)
        else:
            newObject = ShoppingList(food_set_id=newFoodSet)

        newObject.save()
        return displayFoodSet(request, foodSetKind, newFoodSet.id, -1)
    else:
        dict = {"foodSetId": foodSetId, "edit": edit, "foodSet": foodSet, "foodSetKind": foodSetKind, "date" : datetime.datetime.now().strftime("%Y-%m-%d")}
        if foodSetKind == "meals" and foodSet != -1:
            for meal in Meal.objects.all():
                if meal.food_set_id == foodSet:
                    dict["date"] = meal.date_of_eating.strftime("%Y-%m-%d")
        return render(request, 'create_food_set.html',
                      dict)


def meals(request, deleteId=-1):
    return foodSets(request, "meals", int(deleteId))

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'mess': 'INVALID CREDENTIALS'})
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def deleteproduct(request, product_id):
    if not request.user.is_authenticated:
        return redirect('/login')
    product = CustomFood.objects.filter(user_id=request.user.id, id=product_id)
    if len(product) > 0:
        product.delete()
    return redirect('/products')

def copyproduct(request, product_id):
    if not request.user.is_authenticated:
        return redirect('/login')
    product = CustomFood.objects.raw('SELECT * FROM foods_customfood LEFT JOIN foods_food ON foods_customfood.food_id = foods_food.id WHERE foods_customfood.user_id=%s AND foods_customfood.id=%s', [request.user.id, product_id])
    if len(product) == 0:
        return redirect('/products')
    choice = product[0]
    details = {}
    details['name'] = choice.name
    details['energy'] = choice.energy
    details['fat'] = choice.fat
    details['protein'] = choice.protein
    details['carb'] = choice.carbohydrate
    return render(request, 'createproduct.html', {'details': details})

def validate_edit(request, product_id, properties):
    othercustom = CustomFood.objects.filter(food__name=request.POST['name']).exclude(id=product_id)
    if othercustom:
        return 'Another of your custom products already uses this name'
    if not properties['name'] and properties['energy'] and properties['protein'] and properties['fat'] and properties['carb']:
        return 'Please fill all fields'
    try:
        properties['energy'] = float(properties['energy'])
        properties['protein'] = float(properties['protein'])
        properties['fat'] = float(properties['fat'])
        properties['carb'] = float(properties['carb'])
    except ValueError:
        return 'Calories, proteins, fats, carbohydrates must be integers or decimal numbers'
    if len(properties['name']) > 80:
        return 'Product name length cannot exceed 80 characters'
    if properties['energy'] > 1000:
        return 'Calories cannot exceed 1000'
    if properties['protein'] + properties['fat'] + properties['carb'] > 100:
        return 'Proteins, fats and carbohydrates cannot sum up to more than 100'
    if properties['energy'] < 0 or properties['protein'] < 0 or properties['fat'] < 0 or properties['carb'] < 0:
        return 'You must provide non-negative values'
    # wszystko ok
    return ''

def editproduct(request, product_id):
    if not request.user.is_authenticated:
        return redirect('/login')
    product = CustomFood.objects.filter(id=product_id, user_id__id=request.user.id)
    if not product:
        return redirect('/products')
    if request.method=='POST':
        properties = {'name': request.POST['name'], 'carb': request.POST['carbohydrate'], 'fat': request.POST['fat'], 'protein': request.POST['protein'], 'energy': request.POST['energy']}
        error_message = validate_edit(request, product_id, properties)
        if error_message:
            return render(request, 'edit_product.html', {'product': product[0], 'mess': error_message})
        to_update = Food.objects.filter(id=product[0].food.id)
        to_update.update(name=properties['name'])
        to_update.update(energy=properties['energy'])
        to_update.update(protein=properties['protein'])
        to_update.update(carbohydrate=properties['carb'])
        to_update.update(fat=properties['fat'])
        return render(request, 'productcreated.html',  {'message': 'Product edited'})
    else:
        return render(request, 'edit_product.html', {'product': product[0]})

def stats(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    start_date = date.today() - datetime.timedelta(days=29)
    end_date = date.today()
    context = {}
    context['title_string'] = "Stats for last 30 days"
    if request.method == 'POST':
        new_start_date = datetime.datetime.strptime(request.POST.get('start_date'), "%Y-%m-%d")
        new_end_date = datetime.datetime.strptime(request.POST.get('end_date'), "%Y-%m-%d")
        if new_start_date + datetime.timedelta(days=29) >= new_end_date:
            start_date = new_start_date
            end_date = new_end_date
            context['title_string'] = "Stats for chosen period"
        else:
            context['mess'] = 'You can pick time period with maximum of 30 days'
    context['date_labels'] = date_label_set_string(start_date, end_date)
    context['energy_string'] = energy_set_string(request, start_date, end_date)
    context['protein_string'] = protein_set_string(request, start_date, end_date)
    context['carbohydrate_string'] = carbohydrate_set_string(request, start_date, end_date)
    context['fat_string'] = fat_set_string(request, start_date, end_date)
    context['planned_energy'] = planned_energy_for_period(request, start_date, end_date)
    context['planned_protein'] = planned_protein_for_period(request, start_date, end_date)
    context['planned_carbohydrate'] = planned_carbohydrate_for_period(request, start_date, end_date)
    context['planned_fat'] = planned_fat_for_period(request, start_date, end_date)
    return render(request, 'stats.html', context)
  