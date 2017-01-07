from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from forms import *
from django.contrib.auth import login as auth_login
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Restaurant, Order
from utils import google_place_details


@csrf_protect
def login(request):

    variables = {
        'form_reg': RestaurantRegisterForm(),
        'form_rest_login': RestaurantLoginForm()
    }

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

            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect('/profile')
            else:
                variables['error'] = 'Login Failed. Incorrect username or password.'
                return render(request,
                              'login.html',
                              variables,
                              )

    if not request.user.is_anonymous:
        variables['restaurant'] = Restaurant.objects.all().filter(user=request.user)

    return render(request,
                  'login.html',
                  variables,
                  )


def place(request):
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

    user = request.user


    location_id = request.GET.get('place_id')

    if not location_id:
        return HttpResponseRedirect('/')

    date = request.GET.get('date')
    num_people = request.GET.get('numPeople')
    time = request.GET.get('time')

    restaurant = Restaurant.objects.all().filter(location_id=location_id)
    if restaurant[0].is_available:
        is_available = 'true'
    else:
        is_available = 'false'

    popularity = restaurant[0].popularity
    if popularity == 0:
        popularity = '<b style="color:green">not busy</b>'
    elif popularity == 1:
        popularity = '<b style="color:orange">busy</b>'
    elif popularity == 2:
        popularity = '<b style="color:red">very busy</b>'

    google_place_data = google_place_details(location_id)

    context = {
        'form_reg': RestaurantRegisterForm(),
        'form_rest_login': RestaurantLoginForm(),
        'google_place_data': google_place_data,
        'menu': menu,
        'date': date,
        'num_people': num_people,
        'time': time,
        'is_available': is_available,
        'popularity': popularity
    }
    if not user.is_anonymous:
        context['restaurant'] = Restaurant.objects.all().filter(user=request.user)

    if not (location_id and Restaurant.objects.all().filter(location_id=location_id)):
        context['error'] = 'We are currently not supporting this location.'
        return render(request, 'login.html', context)

    return render(request, 'place.html', context)


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

@login_required
def shop_orders(request):
    context = {}
    user = request.user
    restaurant = Restaurant.objects.all().filter(user=user)

    if restaurant:
        accepted_orders = Order.objects.all().filter(restaurant=restaurant).filter(status=1)
        completed_orders = Order.objects.all().filter(restaurant=restaurant).filter(status=3)
        total_orders = Order.objects.all().filter(restaurant=restaurant)
        pending_orders = Order.objects.all().filter(restaurant=restaurant).filter(status=0)

        context = {'restaurant_is_available': restaurant[0].is_available,
                   'restaurant_name': restaurant[0].name,
                   'restaurant_pop': restaurant[0].popularity,
                   'accepted_orders': len(accepted_orders),
                   'completed_orders': len(completed_orders),
                   'pending_orders': len(pending_orders),
                   'total_orders': len(total_orders)
                   }
    else:
        context['error'] = True

    return render(request, 'shop_orders.html', context)


@login_required
def profile(request):
    context = {'restaurant': Restaurant.objects.all().filter(user=request.user)}
    user = request.user
    orders = Order.objects.all().filter(user=user)
    context['orders'] = orders

    return render(request, 'profile.html', context)
