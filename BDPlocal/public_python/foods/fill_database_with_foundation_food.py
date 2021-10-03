from django.contrib.auth.models import User, auth
from django.db.models import Q
from .models import *
from datetime import date
import datetime
from .calendar_helper import *
from .stats_helper import *

def fillDatabaseWithFoundationFood():
    with open('../../parsed_foods.csv') as csv_file:
        line_count = 0
        for row in csv_file:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                #print(f'\trow={row}.')
                row = row[1:-1]
                _, name, kcalPer100g, proteinsPer100g, carbsPer100g, fatsPer100g, _, _ = row.split('", "')
                if len(name) <= 80:
                    name = name.lower()
                    line_count += 1
                    #print(line_count, name, kcalPer100g, proteinsPer100g, carbsPer100g, fatsPer100g)
                    new_product =Food(name=name, energy=float(kcalPer100g), protein=float(proteinsPer100g), fat=float(fatsPer100g), carbohydrate=float(carbsPer100g))
                    new_product.save()
                    new_foundation_product = FoundationFood(food=new_product)
                    new_foundation_product.save()
    
        print(f'Processed {line_count} lines.')
