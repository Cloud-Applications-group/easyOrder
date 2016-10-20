from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required


def login(request):
    context = RequestContext(request, {'user': request.user})
    return render_to_response('login.html', context)


@login_required
def homepage(request):
    context = {'user': request.user}
    return render_to_response('homepage.html', context)



