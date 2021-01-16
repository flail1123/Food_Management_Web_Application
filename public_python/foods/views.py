from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth

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
    return render(request, 'products.html')

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