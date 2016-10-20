from django.shortcuts import render

# Create your views here.



def home(request):
    """
    Home page
    :return:
    """
    return render(request, 'homepage.html', {})