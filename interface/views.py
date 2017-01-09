from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from forms import *
from django.contrib.auth import login as auth_login
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Restaurant, Order, Menu
from utils import google_place_details
import json


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
            restaurant = Restaurant.objects.create(
                user=user,
                location_id=form_reg.cleaned_data['location_id'],
                info='{}',
                name=form_reg.cleaned_data['shop_name']
            )
            Menu.objects.create(
                user=user,
                restaurant=restaurant,
                content="{}"
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
    if request.method == 'POST':
        form_order = OrderForm(request.POST)
        if form_order.is_valid():
            user = request.user
            place_id = request.POST['restaurant_name']
            content = json.loads(request.POST['content'])
            people = request.POST['people']
            date = request.POST['date']
            time = request.POST['time']
            amount = content['amount']
            restaurant = Restaurant.objects.all().filter(location_id=place_id)

            Order.objects.create(user=user,
                                 restaurant=restaurant[0],
                                 content=json.dumps(content),
                                 amount=amount,
                                 reservation_date_time=date + ' ' + time,
                                 people=int(people),
                                 )
        return HttpResponseRedirect('/profile')

    user = request.user
    context = {}

    location_id = request.GET.get('place_id')

    if not location_id:
        return HttpResponseRedirect('/')

    date = request.GET.get('date')
    num_people = request.GET.get('numPeople')
    time = request.GET.get('time')

    restaurant = Restaurant.objects.all().filter(location_id=location_id)
    if not restaurant:
        context['error'] = 'We are currently not supporting this location.'
        return render(request, 'login.html', context)

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

    context['form_reg'] = RestaurantRegisterForm()
    context['form_rest_login'] = RestaurantLoginForm()

    google_place_data = google_place_details(location_id)

    if not (google_place_data):
        context['error'] = 'This location is not fully supported yet.'
        return render(request, 'login.html', context)

    context['google_place_data'] = google_place_data
    context['menu'] = json.loads(Menu.objects.all().filter(restaurant=restaurant)[0].content)
    context['date'] = date
    context['num_people'] = num_people
    context['time'] = time
    context['is_available'] = is_available
    context['popularity'] = popularity
    context['order_form'] = OrderForm()
    context['location_id'] = location_id

    if not user.is_anonymous:
        context['restaurant'] = Restaurant.objects.all().filter(user=request.user)

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
        menu = Menu.objects.all().filter(user=user).filter(restaurant=restaurant)

        context = {'restaurant': restaurant,
                   'id': restaurant[0].id,
                   'restaurant_is_available': restaurant[0].is_available,
                   'restaurant_name': restaurant[0].name,
                   'restaurant_pop': restaurant[0].popularity,
                   'accepted_orders': len(accepted_orders),
                   'completed_orders': len(completed_orders),
                   'pending_orders': len(pending_orders),
                   'total_orders': len(total_orders),
                   'menu_id': str(menu[0].id),
                   'menu': str(menu[0].content)
                   }
    else:
        context['error'] = "You do not own a shop mate!"
        return render(request, 'login.html', context)

    return render(request, 'shop_orders.html', context)


@login_required
def profile(request):
    context = {'restaurant': Restaurant.objects.all().filter(user=request.user)}
    user = request.user
    orders = Order.objects.all().filter(user=user)
    context['orders'] = orders

    return render(request, 'profile.html', context)
