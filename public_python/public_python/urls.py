from django.contrib import admin
from django.urls import path, include
import foods

urlpatterns = [
    path('', include('foods.urls')),
    path('admin/', admin.site.urls),
]
