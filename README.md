# food_management_web_application
To use:
```
git clone https://github.com/flail1123/Food_Management_Web_Application.git
cd Food_Management_Web_Application/BDPlocal/
source bin/activate
cd public_python/
python3 manage.py runserver
```
Now open http://127.0.0.1:8000/ in your browser and create your account.

Description:

Django web application for managing user's diet.

User can input their meals to see how much fat, carbs, proteins and calories their meals consist of.
This data is stored to display graphic statistics and to evaluate plans/goals user can create that say how many calories, fat, carbs and proteins user set as their limit.

If future meal are inputted it is possible to AUTOMATICALLY create shopping list for all the items needed to prepare the meals.
Shopping lists can also be created manually.
Most of the features are accessible from convenient calendar.
All data is stored in postgresql database.
