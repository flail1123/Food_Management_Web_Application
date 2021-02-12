# Generated by Django 2.2 on 2021-01-25 13:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0015_component_foodset_meal_recipe_shoppinglist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicplan',
            name='plan_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foods.Plan'),
        ),
        migrations.AlterField(
            model_name='basicplan',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customplan',
            name='plan_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foods.Plan'),
        ),
        migrations.AlterField(
            model_name='customplan',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]