from django.conf.urls import url, include
from interface import views

urlpatterns = (
    url(r'^$', views.login, name='login'),
    url(r'home', views.homepage, name='home'),
    url(r'register', views.register, name='register')
)
