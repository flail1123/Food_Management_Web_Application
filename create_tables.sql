drop table CustomPlan;
drop table Recipe;
drop table OldBasicPlan;
drop table ShoppingList;
drop table Meal;
drop table FoundationFood;
drop table CustomFood;
drop table Component;
drop table Food;
drop table FoodSet;
drop table AppUser;
drop table Plan;

create table Plan(
    plan_id number(7) primary key,
    energy number(5) not null,
    protein number(5, 1) not null,
    carbohydrate number(5, 1) not null,
    fat number(5, 1) not null
);

create table AppUser(
  user_id number(4) primary key,
  username varchar2(40) not null unique,
  password varchar2(255) not null,
  email varchar2(40) not null unique,
  basic_plan_id number(7) references Plan
);

create table CustomPlan(
    user_id number(4) not null references AppUser,
    plan_id number(7) not null references Plan,
    start_date date not null,
    end_date date not null,
    name varchar2(50) not null,
    constraint CustomPlan_dates_ok check (start_date <= end_date)
);

create table OldBasicPlan(
    user_id number(4) not null references AppUser,
    plan_id number(7) not null references Plan,
    start_date date not null,
    end_date date not null,
    constraint OldBasicPlan_dates_ok check (start_date <= end_date)
);

create table Food(
    food_id number(7) primary key,
    name varchar2(150) not null,
    energy number(4) not null,
    protein number(4, 1) not null,
    fat number(4, 1) not null,
    carbohydrate number(4, 1) not null,
    portion_weight number(4, 1) not null,
    portion_name varchar2(50) not null,
    constraint does_it_sum_up_to_less_that_100 check (protein + fat + carbohydrate <= 100)
);

create table FoundationFood(
    food_id number(7) not null references Food
);

create table CustomFood(
    food_id number(7) not null references Food,
    user_id number(4) not null references AppUser
);

create table FoodSet(
    food_set_id number(7) primary key,
    user_id number(4) not null references AppUser,
    name varchar2(150)
);

create table Recipe(
    food_set_id number(7) not null references FoodSet unique
);

create table ShoppingList(
    food_set_id number(7) not null references FoodSet unique
);

create table Meal(
    food_set_id number(7) not null references FoodSet unique,
    date_of_eating date not null
);

create table Component(
    food_set_id number(7) not null references FoodSet,
    food_id number(7) not null references Food,
    weight number(5, 1) not null,
    constraint component_pk primary key (food_set_id, food_id)
);