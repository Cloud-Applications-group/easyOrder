from django.conf.urls import url, include
from interface import views

urlpatterns = (
    url(r'^$', views.login, name='login'),
    url(r'place', views.place, name='place'),
    url(r'register', views.register, name='register'),
    url(r'shoporders', views.shop_orders, name='shop_orders'),
    url(r'profile', views.profile, name='profile')

)
