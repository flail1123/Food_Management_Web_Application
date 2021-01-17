from django.db import models

# Create your models here.

class Food(models.Model):
    name = models.CharField(max_length=200)
    energy = models.DecimalField(max_digits=5, decimal_places=1)
    protein = models.DecimalField(max_digits=5, decimal_places=1)
    fat = models.DecimalField(max_digits=5, decimal_places=1)
    carbohydrate = models.DecimalField(max_digits=5, decimal_places=1)
    user_id = models.IntegerField(null=True)
