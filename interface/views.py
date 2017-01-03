from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from forms import *
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect


def login(request):
    context = RequestContext(request, {'user': request.user})
    return render_to_response('login.html', context)


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


