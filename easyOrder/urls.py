"""easyOrder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from tastypie.api import Api
from interface.api import *



order_resource = RestaurantOrderResource()
restaurant_resource = RestaurantResource()

v1_api = Api(api_name='v1')
v1_api.register(order_resource)
v1_api.register(MenuResource())
v1_api.register(restaurant_resource)
v1_api.register(UserOrderResource())
v1_api.register(UserRestaurantResource())



urlpatterns = [
# APIs
    url(r'^api/', include(v1_api.urls)),
    url(r'^admin/', admin.site.urls),


    url(r'', include('interface.urls', namespace="interface", app_name="interface")),

    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),


]
