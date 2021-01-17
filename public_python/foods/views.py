from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.db.models import Q
from .models import Food

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
            print('password not matching')
            return render(request, 'register.html', {'mess': 'PASSWORDS MUST MATCH'})

        if User.objects.filter(username=username).exists():
            print('Username taken')
            return render(request, 'register.html', {'mess': 'USERNAME ALREADY EXISTS'})

        user = User.objects.create_user(username=username, password=password1, email=email)
        user.save()

        return redirect('/login', {'succ': 'ACCOUNT CREATED'})

    return render(request, 'register.html')

def home(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    return render(request, 'calendar.html')

def products(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    intitle = request.GET.get('inname')
    print(intitle)
    was_checked = True if request.GET.get('onlycustom') else False
    if intitle:
        if request.GET.get('onlycustom'):
            all_products = Food.objects.filter(name__icontains=intitle).filter(user_id=request.user.id).extra(select={'length':'Length(name)'}).order_by('length')[:20]
        else:
            all_products = Food.objects.filter(name__icontains=intitle).filter(Q(user_id__isnull=True) | Q(user_id = request.user.id)).extra(select={'length':'Length(name)'}).order_by('length')[:20]
        #all_products = Food.objects.filter(name__icontains=intitle)[:20]
    elif was_checked:
        all_products = Food.objects.filter(user_id=request.user.id)[:20]
    else:
        all_products = Food.objects.all().filter(user_id__isnull=True)[:20]
    return render(request, 'products.html', {'products' : all_products, 'sustain_check' : was_checked})

def createproduct(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'POST':
        p_name = request.POST['name']
        p_energy = request.POST['energy']
        p_protein = request.POST['protein']
        p_fat = request.POST['fat']
        p_carb = request.POST['carb']
        try:
            p_energy = float(p_energy)
            p_protein = float(p_protein)
            p_fat = float(p_fat)
            p_carb = float(p_carb)
        except ValueError:
            return render(request, 'createproduct.html', {'mess' : 'Calories, proteins, fats, carbohydrates must be integers or decimal numbers'})
        if len(p_name) > 80 or len(p_name) < 1:
            return render(request, 'createproduct.html', {'mess' : 'Food name must be between 1 and 80 characters long'})
        if p_energy > 1000:
            return render(request, 'createproduct.html', {'mess' : 'Calories cannot exceed 1000'})
        if p_protein + p_fat + p_carb > 100:
            return render(request, 'createproduct.html', {'mess' : 'Proteins, fats and carbohydrates cannot sum up to more than 100'})
        if p_energy < 0 or p_protein < 0 or p_fat < 0 or p_carb < 0:
            return render(request, 'createproduct.html', {'mess' : 'You must provide positive values'})
        p_user_id = request.user.id
        if Food.objects.filter(user_id=request.user.id).filter(name=p_name).count() > 0:
            return render(request, 'createproduct.html', {'mess' : 'You already created product with that name'})
        new_product = Food(name=p_name, energy=p_energy, protein=p_protein, fat=p_fat, carbohydrate=p_carb, user_id=p_user_id)
        new_product.save()
        return render(request, 'productcreated.html')
    else:
        return render(request, 'createproduct.html')
    



def calendar(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    return render(request, 'calendar.html')

def plans(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    return render(request, 'plans.html')

def lists(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    return render(request, 'lists.html')

def recipes(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    return render(request, 'recipes.html')

def meals(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    return render(request, 'meals.html')

def stats(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    return render(request, 'stats.html')


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