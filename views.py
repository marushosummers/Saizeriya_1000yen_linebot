from flask import request, redirect, url_for, render_template, flash
from app import app, db
from models import Menu
import random

def get_menus():

    # params
    first_menus = []
    menus = []
    budget = 1000
    calorie = 0
    salt = 0

    # select first food
    while not first_menus:
        rand = random.randrange(0, db.session.query(Menu.id).count()) + 1
        first_menus = db.session.query(Menu).filter(Menu.id==rand, Menu.price <= budget).all()

    # calc
    menus.append(str(first_menus[0].name))
    budget -= int(first_menus[0].price)
    calorie += int(first_menus[0].calorie)
    salt += float(first_menus[0].salt)

    while budget > 0:

        # avalable food candidate
        candidate = db.session.query(Menu).filter(Menu.price <= budget).all()

        # no candidate break
        if not candidate:
            break

        # select food
        rand = random.randrange(0, len(candidate))

        # add to list
        menus.append((candidate[rand].name))

        #calc
        budget -= int(candidate[rand].price)
        calorie += int(candidate[rand].calorie)
        salt += float(candidate[rand].salt)

    budget = 1000 - budget
    menus.append("--------")
    result = "計" + str(budget) + "円　" + str(calorie) + "kcal 塩分" + str(salt) + "g"
    menus.append(result)
    #return render_template('show_menus.html', menus=menus, budget=budget, calorie=calorie, salt=round(salt,1))
    return menus
