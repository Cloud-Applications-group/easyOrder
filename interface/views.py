from django.contrib.auth import authenticate
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from forms import *
from django.contrib.auth import login as auth_login
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from .models import Restaurant


@csrf_protect
def login(request):
    if request.method == 'POST':
        form_reg = RestaurantRegisterForm(request.POST)
        form_log = RestaurantLoginForm(request.POST)
        if form_reg.is_valid():
            user = User.objects.create_user(
                username=form_reg.cleaned_data['username'],
                password=form_reg.cleaned_data['password1'],
            )
            Restaurant.objects.create(
                user=user,
                location_id=form_reg.cleaned_data['location_id'],
                info='{}',
                name=form_reg.cleaned_data['shop_name']
            )
            return HttpResponseRedirect('/')
        elif form_log.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username = username, password = password)
            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect('/home')
            else:
                return HttpResponseRedirect('/')



    variables = {
        'form_reg': RestaurantRegisterForm(),
        'form_rest_login': RestaurantLoginForm()
    }

    return render(request,
                  'login.html',
                  variables,
                  )


@login_required
def homepage(request):
    menu = {
        "menu": [{
            "category": [{
                "title": "Sides",
                "description": "a little something to accompany your meal",
                "items": [
                    {
                        "item_title": "Chips",
                        "item_description": "Our signature triple-fried chips",
                        "item_options": [
                            {"option_name": "Regular", "price": 1.50}
                        ]
                    }, {

                        "item_title": "Chicken Wings",
                        "item_description": "Piri-piri seasoned wings",
                        "item_options": [
                            {"option_name": "Medium", "price": 2.50},
                            {"option_name": "Hot", "price": 2.50},
                            {"option_name": "Super Hot", "price": 2.50}
                        ]
                    }, {

                        "item_title": "Onion rings",
                        "item_description": "Beer-battered onion rings",
                        "item_options": [
                            {"option_name": "Regular", "price": 1.50}
                        ]
                    }
                ]}, {
                "title": "Mains",
                "description": "Big flavour, diner style food",
                "items": [
                    {
                        "item_title": "Burger",
                        "item_description": "A quarter pounder burger served in a brioche bun with a side of chips or wedges",
                        "item_options": [
                            {"option_name": "Beef", "price": 6.50},
                            {"option_name": "Vegetarian", "price": 5.50}
                        ]
                    }, {
                        "item_title": "Hotdog",
                        "item_description": "A 9 inch American-style hotdog served with a side of chips or wedges",
                        "item_options": [
                            {"option_name": "Hotdog", "price": 5.50}
                        ]
                    }, {
                        "item_title": "Pizza",
                        "item_description": "Fully loaded deep-pan pizza",
                        "item_options": [
                            {"option_name": "Pepperoni", "price": 6.00},
                            {"option_name": "BBQ Chicken", "price": 6.00},
                            {"option_name": "Margherita", "price": 4.50}
                        ]
                    }
                ]}, {
                "title": "Drinks",
                "description": "",
                "items": [
                    {
                        "item_title": "Coke",
                        "item_description": "Coca-cola on draught",
                        "item_options": [
                            {"option_name": "Regular", "price": 1.00},
                            {"option_name": "Diet", "price": 1.00}
                        ]
                    }, {
                        "item_title": "Lemonade",
                        "item_description": "",
                        "item_options": [
                            {"option_name": "Regular", "price": 5.50}
                        ]
                    }, {
                        "item_title": "Beer",
                        "item_description": "400cl glass of Peroni Nastro Azzurro",
                        "item_options": [
                            {"option_name": "Peroni", "price": 6.00}
                        ]
                    }
                ]
            }]
        }]
    }
    context = {'user': request.user, 'menu': menu}
    return render_to_response('homepage.html', context)


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = ShopRegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/')
    else:

        form = ShopRegisterForm()

    variables = {
        'form': form
    }

    return render(request,
                  'register.html',
                  variables,
                  )
