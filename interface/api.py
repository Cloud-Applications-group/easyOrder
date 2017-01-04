# myapp/api.py

from django.shortcuts import get_object_or_404
from tastypie.resources import ModelResource, Resource
from interface.models import *
from tastypie.constants import ALL
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie import fields


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

    class Meta:
        queryset = Restaurant.objects.all()
        resource_name = 'restaurant'
        filtering = {
            'name': ALL
        }



class MenuResource(ModelResource):
    restaurant = fields.ToOneField(RestaurantResource, 'restaurant', full=True)
    class Meta:
        queryset = Menu.objects.all()
        resource_name = 'menu'
        filtering = {
           'restaurant': ALL_WITH_RELATIONS
        }
