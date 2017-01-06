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
    context = {'user': request.user}
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
