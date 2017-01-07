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
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render
import json
from .models import Restaurant, Menu
from utils import google_place_details
import jsonschema
from jsonschema import validate
from jsonschema import FormatChecker
from django.core.exceptions import ObjectDoesNotExist


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

    location_id = request.GET.get('place_id')

    if not (location_id and Restaurant.objects.all().filter(location_id=location_id)):
        variables = {
            'form_reg': RestaurantRegisterForm(),
            'form_rest_login': RestaurantLoginForm(),
            'error': 'We are not currently supporting this location'}
        return render(request, 'login.html', variables)

    restaurant = Restaurant.objects.all().filter(location_id=location_id)[0]
    menu2 = Menu.objects.all().filter(restaurant=restaurant)[0].content
    menu2 = json.loads(menu2.decode('string-escape').strip('"'))

    schema = {
      "type": "object",
      "properties": {
        "menu": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "category": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "items": {
                      "type": "array",
                      "items": {
                        "type" : "object",
                        "properties": {
                            "item_title": {"type": "string"},
                            "item_description": {"type": "string"},
                            "item_options": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "option_name": {"type": "string"},
                                        "price": {"type": "number"}
                                    }, "required": ["option_name", "price"]
                                }
                            }
                        },
                        "required": ["item_title", "item_description", "item_options"]
                      }
                    }
                  },
                  "required": ["title", "description", "items"]
                }
              }
            },
            "required": ["category"]
          }
        }
      },
      "required": ["menu"]
    }


    google_place_data = google_place_details(location_id)

    context = {'menu': menu2, 'google_place_data' : google_place_data }
    return render(request, 'homepage.html', context)


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

@csrf_protect
def menu(request):
    if request.method == "POST":
        print json.dumps(request.body)
        restaurant = Restaurant.objects.filter(user=request.user)[:1].get()
        try:
            menu = Menu.objects.all().filter(restaurant=restaurant)[:1].get()
            menu.content = json.dumps(request.body)
            menu.save()
            print "updated"
        except ObjectDoesNotExist:
            menu = Menu.objects.create(
                user = request.user,
                restaurant = restaurant,
                content = json.dumps(request.body)
            )
            menu.save()
            print "created"
        return render_to_response('homepage.html')
    else:
        return render_to_response('menu.html')

@login_required
def shop_orders(request):
    context = {}
    user = request.user
    restaurant = Restaurant.objects.all().filter(user=user)
    if not restaurant:
        context['error'] = True

    return render(request, 'shop_orders.html', context)
