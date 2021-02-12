# Generated by Django 2.2 on 2021-01-24 00:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0011_component_foodset_meal_recipe_shoppinglist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodset',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='meal',
            name='food_set_id',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='food_set_id',
        ),
        migrations.RemoveField(
            model_name='shoppinglist',
            name='food_set_id',
        ),
        migrations.DeleteModel(
            name='Component',
        ),
        migrations.DeleteModel(
            name='FoodSet',
        ),
        migrations.DeleteModel(
            name='Meal',
        ),
        migrations.DeleteModel(
            name='Recipe',
        ),
        migrations.DeleteModel(
            name='ShoppingList',
        ),
    ]