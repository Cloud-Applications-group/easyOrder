# myapp/api.py

from django.shortcuts import get_object_or_404
from tastypie.resources import ModelResource, Resource
from interface.models import *
from tastypie.constants import ALL


class OrderResource(ModelResource):

    def apply_filters(self, request, applicable_filters):

        print request.user
        if request.user.is_anonymous():
            return Order.objects.none()
        order = Order.objects.all().filter(user=request.user)
        return order


    class Meta:
        queryset = Order.objects.all()
        resource_name = 'order'



class RestaurantResource(ModelResource):
    def apply_filters(self, request, applicable_filters):
        return Restaurant.objects.all()

    class Meta:
        queryset = Restaurant.objects.all()
        resource_name = 'restaurant'



class MenuResource(ModelResource):
    def apply_filters(self, request, applicable_filters):
        return Menu.objects.all()

    class Meta:
        queryset = Menu.objects.all()
        resource_name = 'menu'
        filtering = {'restaurant': ALL}
